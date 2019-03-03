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

  var xhr = new XMLHttpRequest();
  var url = "https://localhost:8886/get_alts";
  xhr.open("POST", url, true);
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.onreadystatechange = function () {
      if (xhr.readyState === 4 && xhr.status === 200) {
          var json = JSON.parse(xhr.responseText);
          console.log(json.products);
          chrome.runtime.sendMessage({'message': "newdata", 'products': json.products});
      }
  };
  var data = JSON.stringify({"title": title, "desc": desc});
  xhr.send(data);
}

grabData();

chrome.runtime.onMessage.addListener(
  function(request, sender, sendResponse) {
    if (request.message == 'grabData') {
        grabData();
    }
});