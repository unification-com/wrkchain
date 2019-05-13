
## $__SECTION_NUMBER__.$__SUB_SECTION_NUMBER__ Appendix 1: The Docker Testnet

The SDK generates a Docker composition to support the testing of your WRKChain.

From the root of the repository, the composition can be brought up with:
```bash
docker-compose -f build/docker-compose.yml up --build
```

To learn how to interact with Docker, start here <https://www.docker.com> and
<https://docs.docker.com/compose/>

**Note**: The WRKChain Docker test environment's data is not persistent, and 
should only be used for development and testing purposes.

**Important**: _do not_ run the WRKChain Oracle using the WRKChain's Docker Testnet
 as a source for **production** WRKChain Root Smart Contract.
Once a WRKChain block's hashes have been committed to the WRKChain Root Smart 
Contract by the WRKChain Oracle, they _**cannot be modified**_.
