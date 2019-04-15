
## $__SECTION_NUMBER__.$__SUB_SECTION_NUMBER__ Appendix 1: The Docker Testnet

The SDK generates a Docker composition to support the testing of your WRKChain.

From the root of the repository, the composition can be brought up with:
```bash
docker-compose -f build/docker-compose.yml up --build
```

To learn how to interact with Docker, start here <https://www.docker.com> and
<https://docs.docker.com/compose/>

**Note**: _do not_ run the WRKChain Oracle using the Docker Testnet as a source for
your deployed **production** WRKChain Root Smart Contract.
Once a WRKChain block's hashes have been committed to the WRKChain Root Smart 
Contract by the WRKChain Oracle, they _**cannot be modified**_.

**If testing the WRKChain Oracle is required in addition to testing the WRKChain,
it is recommended to deploy a separate WRKChain Root smart contract on our 
`mainchain testnet`.**
