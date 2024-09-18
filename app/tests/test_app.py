import unittest
import json

from app.app import app

class SignatureTestCase(unittest.TestCase):
    
    def setUp(self):
        # Configura o ambiente de teste
        self.app = app.test_client()
        self.app.testing = True

    def test_create_signature_valid(self):
        response = self.app.post("/create_signature", 
                                 data=json.dumps({
                                     "name": "John Doe",
                                     "phone": "11987654321",
                                     "department": "Engenharia",
                                     "city": "Goiânia",
                                     "state": "Goiás",
                                     "regional": ""
                                 }),
                                 content_type="application/json")


        # Verifica se a resposta contém a chave "image_url"
        response_json = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("image_url", response_json)

    def test_create_signature_missing_fields(self):
        response = self.app.post("/create_signature", 
                                data=json.dumps({
                                    "phone": "11987654321",
                                }),
                                content_type="application/json")

        # Verifica se a resposta tem o status code esperado
        self.assertEqual(response.status_code, 400)
        
        response_json = json.loads(response.data)
        self.assertIn('message', response_json)  
        self.assertEqual(response_json['message'], 'Preencha todos os campos.') 

if __name__ == "__main__":
    unittest.main()