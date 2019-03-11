from workchain_sdk.documentation.sections.section_factory import SectionFactory
from workchain_sdk.documentation.sections.section_bootnode \
    import SectionBootNodesBuilder
from workchain_sdk.documentation.sections.section_installation \
    import SectionInstallationBuilder
from workchain_sdk.documentation.sections.section_network \
    import SectionNetworkBuilder
from workchain_sdk.documentation.sections.section_oracle \
    import SectionOracleBuilder
from workchain_sdk.documentation.sections.section_rpc_nodes \
    import SectionRpcNodesBuilder
from workchain_sdk.documentation.sections.section_setup \
    import SectionSetupBuilder
from workchain_sdk.documentation.sections.section_validators \
    import SectionValidatorsBuilder

factory = SectionFactory()
factory.register_builder('__SECTION_VALIDATORS__',
                         SectionValidatorsBuilder())
factory.register_builder('__SECTION_JSON_RPC_NODES__',
                         SectionRpcNodesBuilder())
factory.register_builder('__SECTION_BOOTNODE__', SectionBootNodesBuilder())
factory.register_builder('__SECTION_INSTALLATION__',
                         SectionInstallationBuilder())
factory.register_builder('__SECTION_NETWORK__', SectionNetworkBuilder())
factory.register_builder('__SECTION_ORACLE__', SectionOracleBuilder())
factory.register_builder('__SECTION_SETUP__', SectionSetupBuilder())
