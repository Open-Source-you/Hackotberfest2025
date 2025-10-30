try:
    from importlib.metadata import (
        version as __version,
    )
except ImportError:
    # TODO: remove once Python 3.7 is no longer supported
    def __version(package_name: str) -> str:  # type: ignore
        from pkg_resources import (
            get_distribution,
        )

        return get_distribution(package_name).version


from .abi import (
    Decodable,
    TypeStr,
)
from .bls import (
    BLSPrivateKey,
    BLSPubkey,
    BLSSignature,
)
from .discovery import (
    NodeID,
)
from .encoding import (
    HexStr,
    Primitives,
)
from .enums import (
    ForkName,
)
from .ethpm import (
    URI,
    ContractName,
    Manifest,
)
from .evm import (
    Address,
    AnyAddress,
    BlockIdentifier,
    BlockNumber,
    ChecksumAddress,
    Hash32,
    HexAddress,
)
from .networks import (
    ChainId,
)

__all__ = (
    "Decodable",
    "TypeStr",
    "BLSPrivateKey",
    "BLSPubkey",
    "BLSSignature",
    "NodeID",
    "HexStr",
    "Primitives",
    "ForkName",
    "ChainId",
    "URI",
    "ContractName",
    "Manifest",
    "Address",
    "AnyAddress",
    "BlockIdentifier",
    "BlockNumber",
    "ChecksumAddress",
    "Hash32",
    "HexAddress",
)

__version__ = __version("eth-typing")
