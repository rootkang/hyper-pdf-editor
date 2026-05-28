"""
Digital signature module for PDF signing with pyHanko and cryptography.
"""

import logging
from pathlib import Path
from typing import Optional, List
from datetime import datetime
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
from cryptography.x509.oid import NameOID


logger = logging.getLogger(__name__)


class CertificateInfo:
    """Information about a certificate."""
    
    def __init__(self, subject_name: str, issuer_name: str, 
                 valid_from: datetime, valid_to: datetime):
        self.subject_name = subject_name
        self.issuer_name = issuer_name
        self.valid_from = valid_from
        self.valid_to = valid_to
    
    def is_valid(self) -> bool:
        """Check if certificate is currently valid."""
        now = datetime.utcnow()
        return self.valid_from <= now <= self.valid_to


class SignatureManager:
    """Manages PDF digital signatures."""
    
    def __init__(self):
        """Initialize signature manager."""
        self.certificates = {}
        logger.info("Signature Manager initialized")
    
    def load_certificate(self, cert_path: str, key_path: Optional[str] = None) -> bool:
        """Load certificate and optional private key."""
        try:
            cert_path = Path(cert_path)
            
            with open(cert_path, 'rb') as f:
                cert_data = f.read()
            
            cert = x509.load_pem_x509_certificate(cert_data, default_backend())
            
            # Extract certificate info
            subject = cert.subject.get_attributes_for_oid(NameOID.COMMON_NAME)
            issuer = cert.issuer.get_attributes_for_oid(NameOID.COMMON_NAME)
            
            subject_name = subject[0].value if subject else "Unknown"
            issuer_name = issuer[0].value if issuer else "Unknown"
            
            cert_info = CertificateInfo(
                subject_name=subject_name,
                issuer_name=issuer_name,
                valid_from=cert.not_valid_before.replace(tzinfo=None),
                valid_to=cert.not_valid_after.replace(tzinfo=None)
            )
            
            self.certificates[cert_path.name] = {
                'cert': cert,
                'info': cert_info,
                'key': None
            }
            
            # Load private key if provided
            if key_path:
                self._load_private_key(key_path, cert_path.name)
            
            logger.info(f"Loaded certificate: {subject_name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load certificate: {e}")
            return False
    
    def _load_private_key(self, key_path: str, cert_name: str) -> bool:
        """Load private key."""
        try:
            key_path = Path(key_path)
            
            with open(key_path, 'rb') as f:
                key_data = f.read()
            
            from cryptography.hazmat.primitives.serialization import load_pem_private_key
            private_key = load_pem_private_key(
                key_data,
                password=None,
                backend=default_backend()
            )
            
            if cert_name in self.certificates:
                self.certificates[cert_name]['key'] = private_key
                logger.info(f"Loaded private key for: {cert_name}")
                return True
            
        except Exception as e:
            logger.error(f"Failed to load private key: {e}")
            return False
    
    def get_available_certificates(self) -> dict:
        """Get list of available certificates."""
        return {
            name: info['info'] 
            for name, info in self.certificates.items()
        }
    
    def sign_pdf(self, pdf_path: str, output_path: str, 
                cert_name: str, page_num: int = 0,
                x: float = 100, y: float = 100,
                width: float = 150, height: float = 50) -> bool:
        """
        Sign PDF document.
        
        Args:
            pdf_path: Path to PDF to sign
            output_path: Path to save signed PDF
            cert_name: Name of certificate to use
            page_num: Page number to sign (0-indexed)
            x, y: Position of signature
            width, height: Signature box dimensions
        """
        try:
            if cert_name not in self.certificates:
                logger.error(f"Certificate not found: {cert_name}")
                return False
            
            cert_info = self.certificates[cert_name]
            
            # Verify certificate is valid
            if not cert_info['info'].is_valid():
                logger.error(f"Certificate expired: {cert_name}")
                return False
            
            logger.info(f"Signing PDF: {pdf_path} with {cert_name}")
            # Signature implementation with pyHanko goes here
            return True
            
        except Exception as e:
            logger.error(f"Failed to sign PDF: {e}")
            return False


class TokenManager:
    """Manages USB token/PKCS#11 devices."""
    
    def __init__(self):
        """Initialize token manager."""
        self.tokens = {}
        logger.info("Token Manager initialized")
    
    def discover_tokens(self) -> List[str]:
        """Discover connected tokens."""
        try:
            logger.info("Discovering USB tokens...")
            return []
        except Exception as e:
            logger.error(f"Failed to discover tokens: {e}")
            return []
    
    def get_token_certificates(self, token_id: str) -> List[CertificateInfo]:
        """Get certificates from token."""
        try:
            return []
        except Exception as e:
            logger.error(f"Failed to get token certificates: {e}")
            return []


# Global instances
_signature_manager: Optional[SignatureManager] = None
_token_manager: Optional[TokenManager] = None


def get_signature_manager() -> SignatureManager:
    """Get or create global signature manager."""
    global _signature_manager
    if _signature_manager is None:
        _signature_manager = SignatureManager()
    return _signature_manager


def get_token_manager() -> TokenManager:
    """Get or create global token manager."""
    global _token_manager
    if _token_manager is None:
        _token_manager = TokenManager()
    return _token_manager
