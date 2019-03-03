angular.module('popup')
  .controller('MainController', ['$scope', function($scope) {
      $scope.welcomeMsg = "KindShopper";
      $scope.products = [];

      $scope.show_options = function(){
      };

      $scope.contribute = function() {
        chrome.tabs.create({
          url: 'https://github.com/ericzhao28/hacktech2019'
        })
      };
      chrome.runtime.onMessage.addListener(
        function(request, sender, sendResponse) {
        $scope.$apply(function () {
             $scope.products = request.products;
        });
      });

      chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
        var currTab = tabs[0];
        if (currTab) {
            chrome.tabs.sendMessage(currTab.id, {
              message: 'grabData'
            });
        }
      });

  }])
;
