pragma solidity  >=0.8.0;
// SPDX-License-Identifier: MIT

contract CarRental {
mapping(address => carInfo) cars; /* address should be for owner */
mapping(address => rentInfo) renters; /* address should be for owner and customer customer */ 

struct carInfo{
    uint carid;
    string car_info;
    string additional;
    uint price;
    bool isRented;
    bool allowedToUse;
        }

struct rentInfo {
    address payable owner;
    address customer;
    uint carid; /* if carid is 0, the renting expired */ 
    string begindate;
    string enddate;
    string region;

}

    function setCar(uint _carId, string memory _car_info, string memory _additional, uint _price) public {
        cars[msg.sender] = carInfo({carid: _carId, car_info: _car_info,additional: _additional,
            price: _price, isRented: false, allowedToUse: true
        });

}
 
   function getCarInfo() public view returns (carInfo memory) {
      return cars[msg.sender];
   }


/*maybe for security, require that only the owner can edit who is the owner and customer in HIS rentInfo and same for customer, making 2 seperate functions*/ 
/* require(renters[msg.sender].customer == msg.sender , "Only the customer can edit this"); */ 

function setRenters(address payable _owner, address _customer, uint _carid, string memory _begindate, string memory _enddate, string memory _region) public {
    renters[msg.sender] = rentInfo({


        owner: _owner,
        customer: _customer,
        carid: _carid ,
    begindate: _begindate,
    enddate: _enddate,
    region: _region
    });
}


function getRenters() public view returns (address owner, address customer, uint carid, string memory begindate, string memory enddate, string memory region) {
    rentInfo storage r = renters[msg.sender];
    return (r.owner, r.customer, r.carid, r.begindate, r.enddate, r.region);
}

/* only executed by customer */
   function sendEth() payable public{
     rentInfo storage r = renters[msg.sender];
     require(r.customer == msg.sender && renters[r.owner].customer== msg.sender , "Only the customer can send funds"); 
     uint amount = msg.value;
     r.owner.transfer(amount); /* send money to owner receiver.transfer(amount); */
}


}

/* how to it works */
/* customer and owner agree on car somewhere, then they both write the information of rent (rentInfo) in the contract */
/* then the customer makes the transfer call to sendEth and pays the owner */