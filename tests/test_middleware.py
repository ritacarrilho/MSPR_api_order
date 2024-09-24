import unittest
from unittest.mock import patch
from fastapi import HTTPException, status
from app.middleware import verify_jwt_token, get_current_user, is_admin, is_customer_or_admin
from jose import jwt, JWTError


class TestMiddleware(unittest.TestCase):

    @patch.dict("os.environ", {"SECRET_KEY": "secret", "ALGORITHM": "HS256"})
    def setUp(self):
        self.secret_key = "secret"
        self.algorithm = "HS256"

    # @patch("app.middleware.jwt.decode")
    # def test_verify_jwt_token_valid(self, mock_jwt_decode):
    #     token = "valid_token"
    #     mock_jwt_decode.return_value = {"id_customer": 1, "customer_type": 1}

    #     payload = verify_jwt_token(token)

    #     mock_jwt_decode.assert_called_once_with(token, self.secret_key, algorithms=[self.algorithm])
    #     self.assertEqual(payload, {"id_customer": 1, "customer_type": 1})

    @patch("app.middleware.jwt.decode", side_effect=JWTError)
    def test_verify_jwt_token_invalid(self, mock_jwt_decode):
        token = "invalid_token"

        with self.assertRaises(HTTPException) as context:
            verify_jwt_token(token)

        self.assertEqual(context.exception.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(context.exception.detail, "Could not validate credentials")

    @patch("app.middleware.verify_jwt_token")
    def test_get_current_user(self, mock_verify_jwt_token):
        token = "valid_token"
        mock_verify_jwt_token.return_value = {"id_customer": 1, "customer_type": 1}

        result = get_current_user(token)

        mock_verify_jwt_token.assert_called_once_with(token)
        self.assertEqual(result, {"id_customer": 1, "customer_type": 1})

    @patch("app.middleware.get_current_user")
    def test_is_admin_valid(self, mock_get_current_user):
        current_customer = {"customer_type": 1}
        mock_get_current_user.return_value = current_customer

        try:
            is_admin(current_customer)
        except HTTPException:
            self.fail("is_admin() raised HTTPException unexpectedly!")

    @patch("app.middleware.get_current_user")
    def test_is_admin_invalid(self, mock_get_current_user):
        current_customer = {"customer_type": 2}
        mock_get_current_user.return_value = current_customer

        with self.assertRaises(HTTPException) as context:
            is_admin(current_customer)

        self.assertEqual(context.exception.status_code, status.HTTP_403_FORBIDDEN)

    @patch("app.middleware.get_current_user")
    def test_is_customer_or_admin_valid_admin(self, mock_get_current_user):
        current_customer = {"customer_type": 1, "id_customer": 1}
        mock_get_current_user.return_value = current_customer

        try:
            is_customer_or_admin(current_customer, 2)
        except HTTPException:
            self.fail("is_customer_or_admin() raised HTTPException unexpectedly for admin!")

    @patch("app.middleware.get_current_user")
    def test_is_customer_or_admin_valid_customer(self, mock_get_current_user):
        current_customer = {"customer_type": 2, "id_customer": 1}
        mock_get_current_user.return_value = current_customer

        try:
            is_customer_or_admin(current_customer, 1)
        except HTTPException:
            self.fail("is_customer_or_admin() raised HTTPException unexpectedly for owner!")

    @patch("app.middleware.get_current_user")
    def test_is_customer_or_admin_invalid(self, mock_get_current_user):
        current_customer = {"customer_type": 2, "id_customer": 1}
        mock_get_current_user.return_value = current_customer

        with self.assertRaises(HTTPException) as context:
            is_customer_or_admin(current_customer, 2)

        self.assertEqual(context.exception.status_code, status.HTTP_403_FORBIDDEN)


if __name__ == '__main__':
    unittest.main()
