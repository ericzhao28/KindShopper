'use strict';


chrome.contextMenus.create({
    title: "Thanks for being a kind shopper!",
    id:'selectFromContextMenu',
    contexts: ["all"]
  }, function() {
      var error = chrome.runtime.lastError;
      if(error) {
        console.log(error);
      }
      else {
        console.log('Context menu created');
      }
  });

chrome.tabs.onUpdated.addListener(
  function(tabId, changeInfo, tab) {
    if (changeInfo.url) {
      chrome.tabs.sendMessage( tabId, {
        message: 'grabData', text: ''
      })
    }
  }
);
