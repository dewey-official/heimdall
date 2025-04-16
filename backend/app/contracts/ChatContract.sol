// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

contract ChatContract {
    mapping(address => string[]) public chatRecords;

    event ChatStored(address indexed user, string ipfsHash);

    // 본인만 저장 가능하게 수정
    function storeChat(string memory ipfsHash) public {
        require(bytes(ipfsHash).length < 256, "IPFS hash too long"); // 제한 추가
        chatRecords[msg.sender].push(ipfsHash);
        emit ChatStored(msg.sender, ipfsHash);
    }

    function getChats(address user) public view returns (string[] memory) {
        return chatRecords[user];
    }
}
