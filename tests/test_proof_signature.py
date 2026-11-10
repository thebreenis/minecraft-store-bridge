import base64,struct,unittest
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import encode_dss_signature
from appletv_auth_probe import ProofKey

class ProofSignatureTests(unittest.TestCase):
    def setUp(self):
        self.key=ProofKey()
        self.timestamp=132000000000000000
        self.body=b'{"synthetic":true}'
        self.auth="synthetic-authorization-not-a-token"
        self.signed=base64.b64decode(self.key.sign_request("post","https://example.invalid/path?x=1",self.body,self.auth,self.timestamp))
    def message(self,body):
        return (struct.pack(">I",1)+b"\x00"+struct.pack(">Q",self.timestamp)+b"\x00"+
                b"POST\x00/path?x=1\x00"+self.auth.encode()+b"\x00"+body+b"\x00")
    def der(self):
        return encode_dss_signature(int.from_bytes(self.signed[12:44],"big"),int.from_bytes(self.signed[44:76],"big"))
    def test_wire_size_and_header(self):
        self.assertEqual(len(self.signed),76)
        self.assertEqual(struct.unpack(">IQ",self.signed[:12]),(1,self.timestamp))
    def test_signature_verifies_exact_bytes(self):
        self.key.private_key.public_key().verify(self.der(),self.message(self.body),ec.ECDSA(hashes.SHA256()))
    def test_changed_body_fails(self):
        with self.assertRaises(InvalidSignature):
            self.key.private_key.public_key().verify(self.der(),self.message(b'{"synthetic":false}'),ec.ECDSA(hashes.SHA256()))
