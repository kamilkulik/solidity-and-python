// SPDX-Licence-Identified: MIT

pragma solidity ^0.6.0;

contract SimpleStorage {
    
    // this will get initialised to zero
    uint256 _favouriteNumber;
    
    struct People {
        uint256 favouriteNumber;
        string name;
    }
    
    People[] public people;
    mapping(string => uint256) public nameToFavouriteNumber;
    
    function store(uint256 favouriteNumber) public {
        _favouriteNumber = favouriteNumber;
    }
    
    function retrieve() public view returns(uint256) {
        return _favouriteNumber;
    }
    
    function privateRetrieve() private view returns(uint256) {
        return _favouriteNumber;
    }
    
    function addPerson(string memory name, uint256 favouriteNumber) public {
        people.push(People( favouriteNumber, name ));
        nameToFavouriteNumber[name] = favouriteNumber;
    }
}