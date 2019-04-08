WRKChain SDK
============

This directory contains everything required to get started running a WRKChain. 

Please refer to either the generated `documentation.html` or `documentation.md` 
located in this directory for further information on installing and 
running your WRKChain.

**Reconfiguring your Environment**

**Note**: Unless modifications are made to the configuration file, 
there is no need to run this SDK more than once. The files generated in the
`build` directory can be packaged and distributed to all hosts in the
configuration.

If reconfiguration is required, a complete configuration file, containing all 
defaults and overrides has been generated in `generated_config.json`. This can 
be used to reconfigure your WRKChain environment. Copy the contents of 
`generated_config.json`, edit as required and pass it to the SDK as input.

Subsequent SDK reconfiguration and execution will require the `build` files to 
be repackaged and redistributed to the host machines.
