angular.module('popup')
  .controller('MainController', ['$scope', function($scope) {
      $scope.welcomeMsg = "KindShopper";
      $scope.products = [
        {"image_url": "http://thumbs1.ebaystatic.com/m/mF0SrqCyWfPRoYbXPvvIbCA/140.jpg",
         "title": "Patagonia SS Men's",
         "deal_type": "ecofriendly",
         "desc": "Patagonia SS Men's Size",
         "deal_url": "https://shop.nordstrom.com/s/patagonia-radalie-water-repellent-thermogreen-insulated-jacket/4532643?origin=category-personalizedsort&breadcrumb=Home%2FBrands%2FPatagonia%2FWomen%2FOuterwear%20%26%20Clothing&color=forge%20grey",
         "price": "$43"},
        {"image_url": "http://thumbs1.ebaystatic.com/m/mF0SrqCyWfPRoYbXPvvIbCA/140.jpg",
         "title": "Patagonia SS Men's",
         "deal_type": "charitable",
         "desc": "Patagonia SS Men's Size Medium M Snap Button Polo Shirt Organic Cotton Blend Red",
         "deal_url": "https://shop.nordstrom.com/s/patagonia-radalie-water-repellent-thermogreen-insulated-jacket/4532643?origin=category-personalizedsort&breadcrumb=Home%2FBrands%2FPatagonia%2FWomen%2FOuterwear%20%26%20Clothing&color=forge%20grey",
         "price": "$43"},
        {"image_url": "http://thumbs1.ebaystatic.com/m/mF0SrqCyWfPRoYbXPvvIbCA/140.jpg",
         "title": "Patagonia SS Men's",
         "deal_type": "reused",
         "desc": "Patagonia SS Men's Size Medium M Snap Button Polo Shirt Organic Cotton Blend Red",
         "deal_url": "https://shop.nordstrom.com/s/patagonia-radalie-water-repellent-thermogreen-insulated-jacket/4532643?origin=category-personalizedsort&breadcrumb=Home%2FBrands%2FPatagonia%2FWomen%2FOuterwear%20%26%20Clothing&color=forge%20grey",
         "price": "$43"},
       ];

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
