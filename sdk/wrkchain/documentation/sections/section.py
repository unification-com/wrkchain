from wrkchain.documentation.sections.section_factory import SectionFactory
from wrkchain.documentation.sections.section_bootnode \
    import SectionBootNodesBuilder
from wrkchain.documentation.sections.section_installation \
    import SectionInstallationBuilder
from wrkchain.documentation.sections.section_network \
    import SectionNetworkBuilder
from wrkchain.documentation.sections.section_oracle \
    import SectionOracleBuilder
from wrkchain.documentation.sections.section_setup \
    import SectionSetupBuilder
from wrkchain.documentation.sections.section_nodes \
    import SectionNodesBuilder
from wrkchain.documentation.sections.section_introduction \
    import SectionIntroductionBuilder
from wrkchain.documentation.sections.section_glossary \
    import SectionGlossaryBuilder
from wrkchain.documentation.sections.section_appendices \
    import SectionAppendicesBuilder

section_factory = SectionFactory()
section_factory.register_builder(
    '__SECTION_BOOTNODE__', SectionBootNodesBuilder())
section_factory.register_builder(
    '__SECTION_INSTALLATION__', SectionInstallationBuilder())
section_factory.register_builder('__SECTION_NETWORK__',
                                 SectionNetworkBuilder())
section_factory.register_builder('__SECTION_ORACLE__', SectionOracleBuilder())
section_factory.register_builder('__SECTION_SETUP__', SectionSetupBuilder())
section_factory.register_builder('__SECTION_NODES__', SectionNodesBuilder())
section_factory.register_builder('__SECTION_INTRODUCTION__',
                                 SectionIntroductionBuilder())
section_factory.register_builder('__SECTION_GLOSSARY__',
                                 SectionGlossaryBuilder())
section_factory.register_builder('__SECTION_APPENDICES__',
                                 SectionAppendicesBuilder())
