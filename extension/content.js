function displayRestaurantPopup() {
    console.log("Checking for restaurant name...");
  
    // Inject Google Fonts link for IBM Plex Sans
    if (!document.getElementById("ibm-plex-sans-font")) {
      const fontLink = document.createElement("link");
      fontLink.id = "ibm-plex-sans-font";
      fontLink.rel = "stylesheet";
      fontLink.href = "https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400&display=swap";
      document.head.appendChild(fontLink);
    }
  
    const placePageNameElement = document.querySelector('h1.DUwDvf.lfPIob');
    if (placePageNameElement) {
      console.log("Restaurant name found:", placePageNameElement.textContent.trim());
  
      if (!document.getElementById("restaurant-popup")) {
        const restaurantName = placePageNameElement.textContent.trim();
  
        // Create a popup container
        const popup = document.createElement("div");
        popup.id = "restaurant-popup";
        popup.style.cssText = `
          position: fixed;
          top: 56px;
          right: 20px;
          padding: 15px;
          background: white;
          color: black;
          border-radius: 8px;
          font-family: 'IBM Plex Sans', sans-serif;
          font-size: 14px;
          z-index: 99999;
          box-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
        `;
  
        // Create the heading element
        const heading = document.createElement("h2");
        heading.innerText = "Binge";
        heading.style.cssText = `
          margin: 0 0 10px 0;
          text-align: center;
          font-size: 18px;
          color: black;
        `;
  
        // Create the restaurant name element
        const nameElement = document.createElement("div");
        nameElement.innerText = `Restaurant: ${restaurantName}`;
        nameElement.style.cssText = `
          font-size: 14px;
          text-align: left;
        `;
  
        // Create the button element
        const matchButton = document.createElement("button");
        matchButton.innerText = "Look for Match";
        matchButton.style.cssText = `
          display: block;
          margin: 10px auto;
          padding: 8px 20px;
          background-color: black;
          color: white;
          border: none;
          border-radius: 20px;
          cursor: pointer;
          font-size: 14px;
        `;
        matchButton.addEventListener("click", () => {
            console.log("Match button clicked for", restaurantName);
            const targetUrl = "http://www.bingeeating.study/restaurant"; // Flask backend URL
            const encodedRestaurantName = encodeURIComponent(restaurantName);
            const finalUrl = `${targetUrl}?name=${encodedRestaurantName}`;
          
            console.log("Opening new tab with URL:", finalUrl);
            window.open(finalUrl, "_blank"); // Open the URL in a new tab
        });
  
        // Append the heading, restaurant name, and button to the popup
        popup.appendChild(heading);
        popup.appendChild(nameElement);
        popup.appendChild(matchButton);
        document.body.appendChild(popup);
        console.log("Popup appended to the DOM");
  
        setTimeout(() => {
          popup.remove();
        }, 1000); // 1 seconds
      }
    } else {
      console.log("No restaurant name found.");
    }
  }
  
  const observer = new MutationObserver(displayRestaurantPopup);
  observer.observe(document.body, { childList: true, subtree: true });
  
  displayRestaurantPopup();