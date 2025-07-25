console.log(carData); // This will log the carData object
console.log(formattedMakes); // This will log the formatted makes object

document.addEventListener("DOMContentLoaded", () => {
    const allMakes = Object.keys(carData); // Get all makes from carData

    const makeInput = document.getElementById("make");
    const dropdown = document.getElementById("makeDropdown");

    let filtered = [];
    let selectedIndex = -1;

    function filterDropdown() {
        const typed = makeInput.value.toLowerCase();
        dropdown.innerHTML = "";
        selectedIndex = -1; // Reset selected index

        filtered = allMakes.filter(make => make.startsWith(typed));

        filtered.forEach(make => {
            const item = document.createElement("div");
            item.className = "px-4 py-2 hover:bg-blue-600 cursor-pointer";
            item.textContent = formattedMakes[make];
            item.onclick = () => {
                makeInput.value = formattedMakes[make];;
                dropdown.classList.add("hidden");
                document.getElementById("model").focus(); // Move focus to model input
                makeInput.dispatchEvent(new Event("change"));
            };
            dropdown.appendChild(item);
        });

        dropdown.classList.toggle("hidden", filtered.length === 0);
    }

    function updateHighlightedItem() {
        const items = dropdown.querySelectorAll("div");
        items.forEach((item, index) => {
            item.classList.toggle("bg-blue-600", index === selectedIndex);
            item.classList.toggle("text-white", index === selectedIndex);
        });
    }

    function showDropdown() {
        // if(makeInput.value.trim() !== "") {
        //     filterDropdown();
        // }
        filterDropdown();
    }

    function hideDropdown() {
        setTimeout(() => {
            dropdown.classList.add("hidden");
        }, 100);
    }

    makeInput.addEventListener("input", filterDropdown);
    makeInput.addEventListener("focus", showDropdown);
    makeInput.addEventListener("blur", hideDropdown);

    makeInput.addEventListener("keydown", (e) => {
        const items = dropdown.querySelectorAll("div");

        if (e.key === "ArrowDown") {
            e.preventDefault(); // Prevent default scrolling due to arrow keys
            if (selectedIndex < items.length - 1) {
                selectedIndex++;
                updateHighlightedItem();
            }
        } else if (e.key === "ArrowUp") {
            e.preventDefault();
            if (selectedIndex > 0) {
                selectedIndex--;
                updateHighlightedItem();
            }
        } else if (e.key === "Enter") {
            e.preventDefault(); // Prevent form submission
            if (selectedIndex >= 0 && items[selectedIndex]) {
                items[selectedIndex].click(); // Simulate click on highlighted item
                document.getElementById("model").focus(); // Move focus to model input
            }
        }
    });

    modelInput = document.getElementById("model");
    modelInput.addEventListener("keydown", (e) => {
        if (e.key ==="Enter") {
            // Submit form 
            document.getElementById("searchButton").click();
        }
    });

    makeInput.addEventListener("change", () => {
        const selectedMake = makeInput.value.toLowerCase();
        const modelSelect = document.getElementById("model");
        modelSelect.innerHTML = "";

        const defaultOption = document.createElement("option");
        defaultOption.value = "";
        defaultOption.text = "Select Model";
        modelSelect.appendChild(defaultOption);

        if(carData[selectedMake]) {
            carData[selectedMake].forEach(model => {
                const option = document.createElement("option");
                option.value = model;
                option.text = model.charAt(0).toUpperCase() + model.slice(1); // Capitalize first letter
                modelSelect.appendChild(option);
            });
        }
    });
});


// // Create a data list for makes
// document.addEventListener("DOMContentLoaded", () => { // Wait for DOM to load
//     const makeInput = document.getElementById("make");
//     const makeList = document.getElementById("make-list");


//     updateDataList();

//     makeInput.addEventListener("input", (e) => { // Listen for input changes
//         const typed = e.target.value.toLowerCase();
//         updateDataList(typed);
//     });

//     function updateDataList(filter) {
//         makeList.innerHTML = "";
//         const filteredMakes = allMakes.filter(make => make.startsWith(filter));

//         // Create options for each make
//         filteredMakes.forEach(make => {
//             const option = document.createElement("option");
//             option.value = make;
//             makeList.appendChild(option);
//         });
//     }

//     // Update models when make changes
//     makeInput.addEventListener("change", () => {
//         const selectedMake = makeInput.value.toLowerCase();
//         const modelSelect = document.getElementById("model");
//         modelSelect.innerHTML = "";

//         if(carData[selectedMake]){ // Check if make exists
//             carData[selectedMake].forEach(function (model) { // Loop through models
//             const option = document.createElement("option"); // Create new option element
//             option.value = model; // Set value to model
//             option.text = model.charAt(0).toUpperCase() + model.slice(1); // Capitalize first letter
//             modelSelect.appendChild(option); // Append option to model select
//             });
//         }
//     });
// });

// For basic dropdown functionality
// function updateModels(){
//     const makeSelect = document.getElementById("make");
//     const modelSelect = document.getElementById("model");
//     const selectedMake = makeSelect.value;

//     modelSelect.innerHTML = ""; // Clear previous options

    // if(carData[selectedMake]){ // Check if make exists
    //     carData[selectedMake].forEach(function (model) { // Loop through models
    //         const option = document.createElement("option"); // Create new option element
    //         option.value = model; // Set value to model
    //         option.text = model.charAt(0).toUpperCase() + model.slice(1); // Capitalize first letter
    //         modelSelect.appendChild(option); // Append option to model select
    //     });
    // }
// }