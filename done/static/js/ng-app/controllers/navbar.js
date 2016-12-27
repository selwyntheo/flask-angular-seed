angular.module('MyApp')
  .controller('NavbarCtrl', function($scope, $q,$auth) {
    $scope.isAuthenticated = function() {
      return $auth.isAuthenticated();
    };
   
  });
