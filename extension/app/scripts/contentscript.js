let grabData = function() {
  let title_elem = document.querySelector('[itemprop="name"]');
  let desc_elem = document.querySelector('[data-element="selling-statement"]');
  if ((title_elem == null) || (desc_elem == null)) {
    console.log("No match");
    return;
  }

  let title = title_elem.textContent;
  console.log("Title " + title);
  let desc = desc_elem.textContent;
  console.log("Desc " + desc);

  $http.post("http://localhost:5000/get_products", {"title": title, "desc": desc}, {headers: {'Content-Type': 'application/json'} })
  .then(function (response) {
      console.log(response.data);
      chrome.runtime.sendMessage({'message': "newdata", 'products': response.data});
  });


}

grabData();

chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    if (request.message == 'grabData') {
        grabData();
    }
});