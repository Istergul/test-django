'use strict';

var module = angular.module('app', [
    'ngCookies'
])

.config(function($interpolateProvider){
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
})

.run( function run($http, $cookies){
    $http.defaults.headers.post['X-CSRFToken'] = $cookies['csrftoken'];
})

.service('userService', ['$http', '$q', 'dateFilter', function($http, $q, dateFilter) {

    this.getUsers = function() {
        return $http.get("api/get-users", {});
    };
    this.addUser = function(newUser) {
        var user = angular.copy(newUser);
        user['date_joined'] = dateFilter(newUser.date_joined, 'yyyy.MM.dd');
        return $http.post("api/add-user", user);
    };
    this.updateUser = function(user) {
        return $http.post("api/update-user", user);
    };

}])

.service('roomService', ['$http', '$q', function($http, $q) {

    this.getRooms = function() {
        return $http.get("api/get-rooms", {});
    };
    this.addRoom = function(newRoom) {
        return $http.post("api/add-room", newRoom);
    };
    this.updateRoom = function(room) {
        return $http.post("api/update-room", room);
    };

}])

.controller('ContainerCtrl', ["$scope", "$rootScope", function($scope, $rootScope) {
    $scope.activeTab = "users";
    $scope.selectTab = function(tab, $event) {
        $scope.activeTab = tab;
        $event.preventDefault();
    };
}])

.controller('UserCtrl', ["$scope", "$rootScope", "$http", "$q", "userService", "dateFilter", function($scope, $rootScope, $http, $q, userService, dateFilter) {

    $scope.addNewUser = function(newUser) {
        userService.addUser(newUser).then(
            function (data) {
                $scope.users.push(data.data.result);
                console.log('send yes', data);
            },
            function (data) {
                console.log('send no', data);
            }
        );
    };

    $scope.users = [];

    userService.getUsers().then(
        function (data) {
            console.log('success', data);
            $scope.users = data.data.result;
        },
        function (data) {
            console.log('error', data);
        }
    );

    $scope.showError = function(ngModelController, error) {
//        console.log(ngModelController.$error);
        return ngModelController.$dirty && ngModelController.$error[error];
    };

    $scope.canSave = function() {
        return $scope.newUserForm.$dirty && $scope.newUserForm.$valid;
    };

    $scope.showGrid = {};
    $scope.isShowField = function(userID, field) {
        if ($scope.showGrid.hasOwnProperty(userID)
                && $scope.showGrid[userID].hasOwnProperty(field)
                && $scope.showGrid[userID][field]) {
            return true;
        } else {
            return false;
        }
    };
    $scope.updateField = function(user, field) {
        var val = {};
        val[field] = true;
        $scope.showGrid[user.id] = val;
    };

    $scope.updateUser = function(user, field, $event) {
        if ($event.keyCode === 13) {
            console.log(user);
            if (field === 'date_joined') {
                if (!user['date_joined'])
                    return;
                user['date_joined'] = dateFilter(user.date_joined, 'yyyy.MM.dd');
            }
            userService.updateUser(user).then(
                function(data) {
                    var val = {};
                    val[field] = false;
                    $scope.showGrid[user.id] = val;
                },
                function(data) {
                    console.log('error', data);
                }
            );
        }
    };

}])

.controller('RoomCtrl', ["$scope", "$rootScope", "$http", "$q", "roomService", function($scope, $rootScope, $http, $q, roomService) {

    $scope.addNewRoom = function(newRoom) {
        roomService.addRoom(newRoom).then(
            function (data) {
                $scope.rooms.push(data.data.result);
                console.log('send yes', data);
            },
            function (data) {
                console.log('send no', data);
            }
        );
    };

    $scope.rooms = [];

    roomService.getRooms().then(
        function (data) {
            console.log('success', data);
            $scope.rooms = data.data.result;
        },
        function (data) {
            console.log('error', data);
        }
    );

    $scope.showError = function(ngModelController, error) {
//        console.log(ngModelController.$error);
        return ngModelController.$dirty && ngModelController.$error[error];
    };

    $scope.canSave = function() {
        return $scope.newRoomForm.$dirty && $scope.newRoomForm.$valid;
    };

    $scope.showGrid = {};
    $scope.isShowField = function(roomID, field) {
        if ($scope.showGrid.hasOwnProperty(roomID)
                && $scope.showGrid[roomID].hasOwnProperty(field)
                && $scope.showGrid[roomID][field]) {
            return true;
        } else {
            return false;
        }
    };
    $scope.updateField = function(room, field) {
        var val = {};
        val[field] = true;
        $scope.showGrid[room.id] = val;
    };

    $scope.updateRoom = function(room, field, $event) {
        if ($event.keyCode === 13) {
            console.log(room);
            roomService.updateRoom(room).then(
                function(data) {
                    var val = {};
                    val[field] = false;
                    $scope.showGrid[room.id] = val;
                },
                function(data) {
                    console.log('error', data);
                }
            );
        }
    };

}]);
