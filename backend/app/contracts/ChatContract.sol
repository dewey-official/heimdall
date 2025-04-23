// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

contract ChatContract {
    mapping(address => string[]) private chatRecords;

    event ChatStored(address indexed user, string ipfsHash);

    function storeChat(string memory ipfsHash) external {
        require(bytes(ipfsHash).length < 256, "IPFS hash too long");
        chatRecords[msg.sender].push(ipfsHash);
        emit ChatStored(msg.sender, ipfsHash);
    }

    function getChats(address user) external view returns (string[] memory) {
        return chatRecords[user];
    }
}
