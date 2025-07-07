import inject

from app.config import get_config
from app.db.db import Database
from app.services.allocation_service import AllocationService
from app.services.credential_generator import VerifiableCredentialGenerator
from app.services.revokation_service import RevocationService


def container_config(binder: inject.Binder) -> None:
    config = get_config()

    db = Database(config.database)
    binder.bind(Database, db)

    a_svc = AllocationService(db)
    binder.bind(AllocationService, a_svc)

    r_svc = RevocationService(db)
    binder.bind(RevocationService, r_svc)

    vcg_svc = VerifiableCredentialGenerator(config.credential, r_svc)
    binder.bind(VerifiableCredentialGenerator, vcg_svc)


def get_database() -> Database:
    return inject.instance(Database)


def get_allocation_service() -> AllocationService:
    return inject.instance(AllocationService)


def get_revocation_service() -> RevocationService:
    return inject.instance(RevocationService)


def get_credential_generator() -> VerifiableCredentialGenerator:
    return inject.instance(VerifiableCredentialGenerator)


def setup_container() -> None:
    inject.configure(container_config, once=True)
