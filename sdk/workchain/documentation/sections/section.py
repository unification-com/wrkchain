from workchain.documentation.sections.section_factory import SectionFactory
from workchain.documentation.sections.section_bootnode \
    import SectionBootNodesBuilder
from workchain.documentation.sections.section_installation \
    import SectionInstallationBuilder
from workchain.documentation.sections.section_network \
    import SectionNetworkBuilder
from workchain.documentation.sections.section_oracle \
    import SectionOracleBuilder
from workchain.documentation.sections.section_setup \
    import SectionSetupBuilder
from workchain.documentation.sections.section_nodes \
    import SectionNodesBuilder

section_factory = SectionFactory()
section_factory.register_builder('__SECTION_BOOTNODE__', SectionBootNodesBuilder())
section_factory.register_builder('__SECTION_INSTALLATION__',
                                 SectionInstallationBuilder())
section_factory.register_builder('__SECTION_NETWORK__', SectionNetworkBuilder())
section_factory.register_builder('__SECTION_ORACLE__', SectionOracleBuilder())
section_factory.register_builder('__SECTION_SETUP__', SectionSetupBuilder())
section_factory.register_builder('__SECTION_NODES__', SectionNodesBuilder())
