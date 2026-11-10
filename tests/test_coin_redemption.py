"""Offline money-delivery tests: temporary journal, mocked session, no real requests."""
import json,tempfile,unittest,uuid
from pathlib import Path
from unittest.mock import Mock,patch
import coin_topup as c
import windows_coin_redemption as w

TX=str(uuid.UUID(int=1))
PENDING=[{'product':c.OFFER,'transaction':TX}]
FIELDS=['secret-token','signature','123456789']
def inventory(amount):
    return {'virtualCurrencyBalances':[{'type':'Minecoin','currencyStack':'Total','amount':amount}]}

class RecoveryTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.patches=[patch.object(c,'JOURNAL',Path(self.temp.name)/'journal.json'),
            patch.object(c,'get_bridge_fields',return_value=FIELDS),
            patch.object(c,'Marketplace'),patch.object(c,'redeem_windows'),
            patch.object(c,'POLL_SECONDS',0),patch.object(c.time,'sleep'),patch.object(c,'WINDOWS_CONTEXT',{'xuid':FIELDS[2],'created':c.time.time()}),patch.object(c,'redeem',return_value={'failed':0,'succeeded':0,'transactionIds':0})]
        self.mocks=[p.start() for p in self.patches]
        for p in self.patches:self.addCleanup(p.stop)
        self.client=self.mocks[2].return_value
        self.client.inventory.return_value=inventory(891)
        self.redeem=self.mocks[3]
        self.redeem.return_value={'failed':0,'succeeded':1,'transactionIds':1}
        self.record={'status':'prepared','attempt':'test','product':c.PRODUCT,'coins':320,
                     'balanceBefore':891,'xuid':FIELDS[2]}
        c.save(self.record)
    def journal(self):return json.loads(c.JOURNAL.read_text())
    def test_repeated_cancel_other_packages_with_background_poll(self):
        c.JOURNAL.unlink()
        for product in list(c.PACKS)*2:
            response=c.handle('PRP3',[],product=product)
            attempt=response.decode().split(':')[1]
            self.assertEqual(c.handle('REC1',[]),b'checkout-open')
            self.assertEqual(self.journal()['status'],'prepared')
            self.assertEqual(c.handle('CAN2',[],attempt=attempt),b'cancelled')
            self.assertEqual(c.handle('CAN2',[],attempt=attempt),b'cancelled')
            self.assertEqual(c.handle('REC1',[]),b'idle')
        self.redeem.assert_not_called()
    def test_stale_cancel_does_not_cancel_next_checkout(self):
        c.JOURNAL.unlink()
        old=c.handle('PRP3',[]).decode().split(':')[1]
        c.handle('CAN2',[],attempt=old)
        new=c.handle('PRP3',[],product='9PD3R529P5XZ').decode().split(':')[1]
        with self.assertRaisesRegex(ValueError,'Stale'):c.handle('CAN2',[],attempt=old)
        self.assertEqual(self.journal()['attempt'],new)
        self.assertEqual(self.journal()['status'],'prepared')
    def test_cancel_rejects_receipt_account_change_and_submitted_payment(self):
        for change,pending in [({},PENDING),({'xuid':'other'},[]),({'officialAttemptStarted':1},[]),({'nativeReceipt':PENDING[0]},[]),({'status':'awaiting receipt'},[])]:
            record={**self.record,**change};c.save(record)
            with self.assertRaises(ValueError):c.handle('CAN2',pending,attempt=record['attempt'])
            self.assertEqual(self.journal(),record)
    def test_success_marker_keeps_missing_receipt_guard(self):
        self.assertEqual(c.handle('TOP2',[],attempt=self.record['attempt']),b'pending')
        self.assertEqual(self.journal()['checkoutResult'],'SucceededOrAlreadyPurchased')
        with self.assertRaises(ValueError):c.handle('CAN2',[],attempt=self.record['attempt'])
        with self.assertRaises(ValueError):c.handle('PRP3',[])
        self.redeem.assert_not_called()
    def test_success_with_receipt_can_redeem(self):
        self.client.inventory.side_effect=[inventory(891),inventory(1211)]
        self.assertEqual(c.handle('TOP2',PENDING,{'collections':'key','purchase':'key'},attempt=self.record['attempt']),b'confirmed')
        self.redeem.assert_called_once()
    def test_empty_wallet_can_prepare_first_purchase(self):
        self.record.update(status='cancelled',attempt=uuid.uuid4().hex);c.save(self.record)
        self.client.inventory.return_value={'virtualCurrencyBalances':[]}
        self.assertEqual(c.handle('PRP2',[],product=c.PRODUCT),b'ready')
        self.assertEqual(self.journal()['balanceBefore'],0)
        self.redeem.assert_not_called()
    def test_missing_or_ambiguous_wallet_is_not_zero(self):
        for inv in ({},{'virtualCurrencyBalances':None},
                    {'virtualCurrencyBalances':[{'type':'Minecoin','currencyStack':'Purchased','amount':10}]},
                    {'virtualCurrencyBalances':inventory(10)['virtualCurrencyBalances']*2},
                    inventory(-1),inventory('10')):
            with self.subTest(inv=inv),self.assertRaises(ValueError):c.balance(inv)
    def test_each_package_preparation_delivery_and_duplicate_protection(self):
        for product,(coins,offer) in c.PACKS.items():
            with self.subTest(product=product):
                c.JOURNAL.unlink(missing_ok=True)
                self.client.inventory.side_effect=None
                self.client.inventory.return_value=inventory(1531)
                self.redeem.reset_mock()
                self.assertEqual(c.handle('PRP2',[],product=product),b'ready')
                self.assertEqual(self.journal()['coins'],coins)
                with self.assertRaises(ValueError):c.handle('PRP2',[],product=product)
                pending=[{'product':offer,'transaction':TX}]
                self.client.inventory.side_effect=[inventory(1531),inventory(1531+coins)]
                self.assertEqual(c.handle('RDM1',pending,{'collections':'key','purchase':'key'}),b'confirmed')
                self.assertEqual(c.handle('REC1',[]),b'settled')
                self.assertEqual(self.journal()['balanceAfter'],1531+coins)
                self.redeem.assert_called_once()
    def test_each_package_rejects_wrong_receipt_or_amount(self):
        for product,(coins,offer) in c.PACKS.items():
            with self.subTest(product=product):
                self.record.update(product=product,coins=coins)
                c.save(self.record)
                self.assertEqual(c.handle('REC1',[{'product':'wrong','transaction':TX}]),b'review')
                self.record['coins']=coins+1;c.save(self.record)
                self.assertEqual(c.handle('REC1',[{'product':offer,'transaction':TX}]),b'review')
        self.redeem.assert_not_called()
    def test_unknown_package_rejected_without_changes(self):
        with self.assertRaises(ValueError):c.handle('PRP2',[],product='unknown')
        self.assertEqual(self.journal(),self.record)
        self.mocks[2].assert_not_called()
    def test_completed_never_redeems_or_rearms(self):
        self.record.update(status='confirmed',balanceAfter=1211);c.save(self.record)
        self.assertEqual(c.handle('REC1',[]),b'settled')
        self.assertEqual(c.handle('TOP1',[]),b'settled')
        with self.assertRaises(ValueError):c.handle('ARM1')
        self.redeem.assert_not_called();self.mocks[2].assert_not_called()
        self.assertEqual(self.journal()['balanceAfter'],1211)
    def test_fresh_prepare_after_delivery_preserves_history(self):
        self.record.update(attempt=uuid.UUID(int=50).hex,status='confirmed',balanceAfter=1211,nativeFulfilled=True)
        c.save(self.record);self.client.inventory.return_value=inventory(1211)
        self.assertEqual(c.handle('PRP1',[]),b'ready')
        new=self.journal()
        self.assertNotEqual(new['attempt'],self.record['attempt'])
        self.assertEqual(new['balanceBefore'],1211)
        old=json.loads((c.JOURNAL.parent/'coin-topup-history'/(self.record['attempt']+'.json')).read_text())
        self.assertEqual(old,self.record)
        with self.assertRaises(ValueError):c.handle('PRP1',[])
        self.redeem.assert_not_called()
    def test_fresh_prepare_blocks_pending_native_purchase(self):
        self.record.update(status='confirmed',balanceAfter=1211);c.save(self.record)
        for pending in (None,PENDING):
            with self.assertRaises(ValueError):c.handle('PRP1',pending)
        self.assertEqual(self.journal(),self.record)
    def test_fresh_prepare_blocks_uncertain_delivery(self):
        for status in ('prepared','awaiting receipt','redeeming','requires reconciliation'):
            self.record['status']=status;c.save(self.record)
            with self.assertRaises(ValueError):c.handle('PRP1',[])
        self.redeem.assert_not_called()
    def test_native_ack_requires_exact_original_transaction(self):
        self.record.update(status='confirmed',nativeReceipt=PENDING[0]);c.save(self.record)
        self.assertEqual(c.handle('RDM1',PENDING,{'collections':'key','purchase':'key'}),b'acknowledge')
        self.assertEqual(c.handle('REC1',[{**PENDING[0],'transaction':str(uuid.UUID(int=2))}]),b'review')
        self.redeem.assert_not_called()
    def test_credit_then_duplicate(self):
        self.client.inventory.side_effect=[inventory(891),inventory(1211)]
        self.assertEqual(c.handle('RDM1',PENDING,{'collections':'key','purchase':'key'}),b'confirmed')
        self.assertEqual(c.handle('REC1',[]),b'settled')
        self.redeem.assert_called_once()
        self.assertEqual(self.journal()['nativeReceipt'],PENDING[0])
        self.assertEqual(self.journal()['balanceAfter'],1211)
    def test_empty_success_is_not_credit(self):
        self.redeem.return_value={'failed':0,'succeeded':0,'transactionIds':0}
        self.assertEqual(c.handle('RDM1',PENDING,{'collections':'key','purchase':'key'}),b'pending')
        self.assertEqual(self.journal()['status'],'requires reconciliation')
    def test_timeout_then_restart_detects_credit_without_replay(self):
        self.redeem.side_effect=TimeoutError()
        self.assertEqual(c.handle('RDM1',PENDING,{'collections':'key','purchase':'key'}),b'pending')
        self.assertEqual(self.journal()['officialAttempts'],1)
        self.client.inventory.return_value=inventory(1211)
        self.assertEqual(c.handle('REC1',[]),b'confirmed')
        self.redeem.assert_called_once()
    def test_crash_with_receipt_remaining_detects_credit(self):
        self.record.update(status='redeeming',nativeReceipt=PENDING[0],officialAttemptStarted=1,officialAttempts=1);c.save(self.record)
        self.client.inventory.return_value=inventory(1211)
        self.assertEqual(c.handle('RDM1',PENDING,{'collections':'key','purchase':'key'}),b'confirmed')
        self.redeem.assert_not_called()
    def test_immediate_retry_does_not_resubmit(self):
        self.redeem.side_effect=TimeoutError()
        self.assertEqual(c.handle('RDM1',PENDING,{'collections':'key','purchase':'key'}),b'pending')
        self.assertEqual(c.handle('RDM1',PENDING,{'collections':'key','purchase':'key'}),b'pending')
        self.redeem.assert_called_once()
    def test_unrelated_receipts_rejected(self):
        for pending in ([{**PENDING[0],'product':'other'}],PENDING*2):
            self.assertEqual(c.handle('REC1',pending),b'review')
        self.redeem.assert_not_called();self.mocks[2].assert_not_called()
    def test_account_change_rejected(self):
        self.record['xuid']='999';c.save(self.record)
        self.assertEqual(c.handle('RDM1',PENDING,{'collections':'key','purchase':'key'}),b'review')
        self.redeem.assert_not_called()
    def test_unexpected_balance_does_not_submit(self):
        self.client.inventory.return_value=inventory(900)
        self.assertEqual(c.handle('RDM1',PENDING,{'collections':'key','purchase':'key'}),b'review')
        self.redeem.assert_not_called()
    def test_missing_receipt_never_submits(self):
        self.assertEqual(c.handle('TOP1',[]),b'pending')
        self.assertEqual(self.journal()['status'],'awaiting receipt')
        self.redeem.assert_not_called()
    def test_no_journal_cannot_redeem_unknown_purchase(self):
        c.JOURNAL.unlink()
        self.assertEqual(c.handle('RDM1',PENDING,{'collections':'key','purchase':'key'}),b'review')
        self.redeem.assert_not_called()
    def test_parser_rejects_malformed_receipts(self):
        self.assertEqual(c.parse_pending(b'0\n'),[])
        self.assertEqual(c.parse_pending(f'1\n{c.OFFER}|{{{TX}}}\n'.encode()),PENDING)
        for data in (b'17\n',b'1\n',b'1\nx|not-a-guid\n',b'-1\n'):
            with self.assertRaises((ValueError,IndexError)):c.parse_pending(data)
    def test_attempt_limit_still_allows_confirming_delayed_credit(self):
        self.record.update(status='requires reconciliation',nativeReceipt=PENDING[0],officialAttemptStarted=1,officialAttempts=3);c.save(self.record)
        self.assertEqual(c.handle('RDM1',PENDING,{'collections':'key','purchase':'key'}),b'review')
        self.client.inventory.return_value=inventory(1211)
        self.assertEqual(c.handle('RDM1',PENDING,{'collections':'key','purchase':'key'}),b'confirmed')
        self.redeem.assert_not_called()
    def test_keys_required_does_not_submit_or_consume_attempt(self):
        self.assertEqual(c.handle('REC1',PENDING),b'keys-required')
        self.assertNotIn('officialAttempts',self.journal())
        self.redeem.assert_not_called()
    def test_failed_windows_request_never_falls_through_to_xbox(self):
        self.redeem.side_effect=TimeoutError()
        self.assertEqual(c.handle('RDM1',PENDING,{'collections':'key','purchase':'key'}),b'pending')
        c.redeem.assert_not_called()
    def test_empty_windows_result_uses_observed_xbox_fallback(self):
        self.redeem.return_value={'failed':0,'succeeded':0,'transactionIds':0}
        c.redeem.return_value={'failed':0,'succeeded':1,'transactionIds':1}
        self.client.inventory.side_effect=[inventory(891),inventory(891),inventory(1211)]
        self.assertEqual(c.handle('RDM1',PENDING,{'collections':'key','purchase':'key'}),b'confirmed')
        c.redeem.assert_called_once()

class RequestTests(unittest.TestCase):
    def test_captured_windows_receipt_contract(self):
        client=Mock(session_id='session')
        client.http.put.return_value.json.return_value={'result':{'failed':[],'succeeded':[],'transactionIds':[]}}
        context={'xuid':FIELDS[2],'collections':'publisher-collections-token'}
        keys={'collections':'c'*200,'purchase':'p'*200}
        w.redeem_windows(client,FIELDS,context,keys)
        args,kw=client.http.put.call_args
        self.assertEqual(args[0],w.ENDPOINT.removesuffix('/xbox'))
        info=kw['json']['purchaseInfo'];receipt=json.loads(info['receipt'])
        self.assertEqual(info['purchasePath'],-1)
        self.assertEqual(info['platformPurchaseId'],'')
        self.assertEqual(info['productSku'],'')
        self.assertEqual(receipt,{'access_token':context['collections'],'actor':'','inventory':'',
            'collections_token':keys['collections'],'purchase_token':keys['purchase'],'sandbox':'RETAIL'})
    def test_secondary_token_configuration(self):
        login=Mock();login.json.return_value={'data':{'EntityToken':{'EntityToken':'entity'}}}
        tokens=Mock();tokens.json.return_value={'data':{'AccessTokens':{'Collections':{'Token':'c'},'Purchase':{'Token':'p'}}}}
        with patch.object(w.requests,'post',side_effect=[login,tokens]) as post:
            context=w.access_tokens(FIELDS)
            self.assertEqual(post.call_args.kwargs['json'],{'MarketplaceConfigInstance':'Secondary','TargetMarketplace':'onestore'})
            self.assertEqual(context['collections'],'c');self.assertEqual(context['purchase'],'p')
            self.assertEqual(context['user'],'anonymous')
    def test_observed_official_contract(self):
        client=Mock(session_id='session')
        client.headers={'Authorization':'franchise-session'}
        client.http.post.return_value.json.return_value={'result':{'failed':[],'succeeded':[],'transactionIds':[]}}
        self.assertEqual(w.redeem(client,FIELDS),{'failed':0,'succeeded':0,'transactionIds':0})
        args,kw=client.http.post.call_args
        self.assertEqual(args,(w.ENDPOINT,))
        self.assertEqual(kw['json']['Redemption'],{'MarketplaceData':{'userId':FIELDS[2],'xboxAuthentication':{'XboxToken':FIELDS[0]}}})
        self.assertEqual(kw['json']['CustomTags']['BuildPlat'],7)
        self.assertEqual(kw['headers'],client.headers)
    def test_malformed_success_is_not_accepted(self):
        client=Mock(session_id='session')
        client.http.post.return_value.json.return_value={'result':{}}
        with self.assertRaises(ValueError):w.redeem(client,FIELDS)

if __name__=='__main__':unittest.main()
