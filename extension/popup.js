// Function to request restaurant names from the content script
function fetchRestaurantNames() {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      const activeTabId = tabs[0].id;
  
      chrome.scripting.executeScript(
        {
          target: { tabId: activeTabId },
          func: () => {
            chrome.runtime.sendMessage({ type: "GET_RESTAURANT_NAMES" }, (response) => {
              const restaurantNames = response.data || [];
              displayRestaurantNames(restaurantNames);
            });
          },
        },
        () => console.log("Script executed")
      );
    });
  }
  
  // Function to display restaurant names in the popup
  function displayRestaurantNames(names) {
    const restaurantList = document.getElementById("restaurant-list");
    restaurantList.innerHTML = ""; // Clear previous names
  
    if (names.length === 0) {
      restaurantList.innerHTML = "<li>No restaurants found</li>";
      return;
    }
  
    names.forEach((name) => {
      const listItem = document.createElement("li");
      listItem.textContent = name;
      restaurantList.appendChild(listItem);
    });
  }
  
  // Fetch restaurant names when the popup is loaded
  document.addEventListener("DOMContentLoaded", fetchRestaurantNames);
  