"use strict";


const API_BASE = "http://127.0.0.1:8000";

let laptops = [];


/* =========================
   Helpers
========================= */

function money(value) {

    return `${Math.round(Number(value)).toLocaleString("en-US")} EGP`;

}


function getBrand(model) {

    const name =
        String(model)
            .toLowerCase();


    if (name.includes("dell")) {
        return "Dell";
    }


    if (name.includes("hp")) {
        return "HP";
    }


    if (name.includes("lenovo")) {
        return "Lenovo";
    }


    return "Other";

}


/* =========================
   Load Inventory
========================= */

async function loadInventory() {

    const table =
        document.getElementById("laptopTable");


    table.innerHTML = `
        <tr>
            <td colspan="6" class="empty">
                Loading inventory...
            </td>
        </tr>
    `;


    try {

        const response =
            await fetch(
                `${API_BASE}/admin/laptops`
            );


        if (!response.ok) {

            throw new Error(
                "Failed to load inventory"
            );

        }


        const data =
            await response.json();


        laptops =
            Array.isArray(data)
                ? data
                : data.laptops || [];


        updateStats();

        renderTable();

    }

    catch (error) {

        table.innerHTML = `
            <tr>
                <td colspan="6" class="empty">
                    Admin inventory API is not connected yet.
                </td>
            </tr>
        `;


        console.error(error);

    }

}


/* =========================
   Stats
========================= */

function updateStats() {

    const prices =
        laptops
            .map(
                laptop =>
                    Number(laptop.price)
            )
            .filter(
                Number.isFinite
            );


    document.getElementById(
        "totalLaptops"
    ).textContent =
        laptops.length;


    if (!prices.length) {

        document.getElementById(
            "avgPrice"
        ).textContent = "—";


        document.getElementById(
            "minPrice"
        ).textContent = "—";


        document.getElementById(
            "maxPrice"
        ).textContent = "—";


        return;

    }


    const average =
        prices.reduce(
            (a, b) => a + b,
            0
        ) / prices.length;


    document.getElementById(
        "avgPrice"
    ).textContent =
        money(average);


    document.getElementById(
        "minPrice"
    ).textContent =
        money(
            Math.min(...prices)
        );


    document.getElementById(
        "maxPrice"
    ).textContent =
        money(
            Math.max(...prices)
        );

}


/* =========================
   Render Table
========================= */

function renderTable() {

    const table =
        document.getElementById(
            "laptopTable"
        );


    const search =
        document.getElementById(
            "searchInput"
        )
        .value
        .toLowerCase()
        .trim();


    const brand =
        document.getElementById(
            "brandFilter"
        ).value;


    const sort =
        document.getElementById(
            "sortFilter"
        ).value;


    let filtered =
        laptops.filter(
            laptop => {

                const model =
                    String(
                        laptop.model || ""
                    )
                    .toLowerCase();


                const matchesSearch =
                    !search ||
                    model.includes(search);


                const matchesBrand =
                    brand === "All" ||
                    getBrand(
                        laptop.model
                    ) === brand;


                return (
                    matchesSearch &&
                    matchesBrand
                );

            }
        );


    if (sort === "low") {

        filtered.sort(
            (a, b) =>
                Number(a.price) -
                Number(b.price)
        );

    }


    if (sort === "high") {

        filtered.sort(
            (a, b) =>
                Number(b.price) -
                Number(a.price)
        );

    }


    if (!filtered.length) {

        table.innerHTML = `
            <tr>
                <td colspan="6" class="empty">
                    No laptops found.
                </td>
            </tr>
        `;

        return;

    }


    table.replaceChildren(

        ...filtered.map(
            laptop => {

                const row =
                    document.createElement(
                        "tr"
                    );


                /* =========================
                   Edit Button
                ========================= */

                const editButton =
                    document.createElement(
                        "button"
                    );


                editButton.className =
                    "edit-btn";


                editButton.type =
                    "button";


                editButton.textContent =
                    "Edit";


                editButton.addEventListener(
                    "click",
                    () =>
                        editLaptop(
                            laptop.code
                        )
                );


                /* =========================
                   Delete Button
                ========================= */

                const deleteButton =
                    document.createElement(
                        "button"
                    );


                deleteButton.className =
                    "delete-btn";


                deleteButton.type =
                    "button";


                deleteButton.textContent =
                    "Delete";


                deleteButton.addEventListener(
                    "click",
                    () =>
                        deleteLaptop(
                            laptop.code
                        )
                );


                /* =========================
                   Model
                ========================= */

                const modelCell =
                    document.createElement(
                        "td"
                    );


                modelCell.className =
                    "model";


                modelCell.textContent =
                    laptop.model || "—";


                /* =========================
                   CPU
                ========================= */

                const cpuCell =
                    document.createElement(
                        "td"
                    );


                cpuCell.textContent =
                    laptop.cpu || "—";


                /* =========================
                   RAM
                ========================= */

                const ramCell =
                    document.createElement(
                        "td"
                    );


                ramCell.textContent =
                    `${laptop.ram ?? "—"} GB`;


                /* =========================
                   GPU
                ========================= */

                const gpuCell =
                    document.createElement(
                        "td"
                    );


                gpuCell.textContent =
                    laptop.gpu_model || "—";


                /* =========================
                   Price
                ========================= */

                const priceCell =
                    document.createElement(
                        "td"
                    );


                priceCell.className =
                    "price";


                priceCell.textContent =
                    money(
                        laptop.price
                    );


                /* =========================
                   Actions
                ========================= */

                const actionsCell =
                    document.createElement(
                        "td"
                    );


                actionsCell.appendChild(
                    editButton
                );


                actionsCell.appendChild(
                    deleteButton
                );


                /* =========================
                   Build Row
                ========================= */

                row.appendChild(
                    modelCell
                );


                row.appendChild(
                    cpuCell
                );


                row.appendChild(
                    ramCell
                );


                row.appendChild(
                    gpuCell
                );


                row.appendChild(
                    priceCell
                );


                row.appendChild(
                    actionsCell
                );


                return row;

            }
        )

    );

}


/* =========================
   Edit
========================= */

function editLaptop(code) {

    const laptop =
        laptops.find(
            item =>
                String(item.code) ===
                String(code)
        );


    if (!laptop) {
        return;
    }


    alert(
        `Edit Laptop\n\n${laptop.model}\n${money(laptop.price)}`
    );

}


/* =========================
   Delete
========================= */

async function deleteLaptop(code) {

    const laptop =
        laptops.find(
            item =>
                String(item.code) ===
                String(code)
        );


    if (!laptop) {
        return;
    }


    const confirmed =
        confirm(
            `Delete Laptop?\n\n` +
            `${laptop.model}\n` +
            `${money(laptop.price)}\n\n` +
            `This action cannot be undone.`
        );


    if (!confirmed) {
        return;
    }


    try {

        const response =
            await fetch(
                `${API_BASE}/admin/laptops/${encodeURIComponent(code)}`,
                {
                    method: "DELETE"
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Failed to delete laptop"
            );

        }


        await loadInventory();


        alert(
            "Laptop deleted successfully ✅"
        );

    }

    catch (error) {

        console.error(error);


        alert(
            "Failed to delete laptop ❌\n\n" +
            error.message
        );

    }

}


/* =========================
   Modal
========================= */

function openModal() {

    const modal =
        document.getElementById(
            "laptopModal"
        );


    const form =
        document.getElementById(
            "laptopForm"
        );


    form.reset();


    modal.classList.remove(
        "hidden"
    );


    setTimeout(
        () => {

            document
                .getElementById(
                    "laptopCode"
                )
                .focus();

        },
        50
    );

}


function closeModal() {

    document
        .getElementById(
            "laptopModal"
        )
        .classList.add(
            "hidden"
        );

}


/* =========================
   Add Laptop
========================= */

async function addLaptop(event) {

    event.preventDefault();


    const saveButton =
        document.querySelector(
            ".save-btn"
        );


    const laptop = {

        code:
            document
                .getElementById(
                    "laptopCode"
                )
                .value
                .trim(),


        model:
            document
                .getElementById(
                    "laptopModel"
                )
                .value
                .trim(),


        cpu:
            document
                .getElementById(
                    "laptopCpu"
                )
                .value
                .trim(),


        ram:
            Number(
                document
                    .getElementById(
                        "laptopRam"
                    )
                    .value
            ),


        gpu_model:
            document
                .getElementById(
                    "laptopGpu"
                )
                .value
                .trim(),


        price:
            Number(
                document
                    .getElementById(
                        "laptopPrice"
                    )
                    .value
            )

    };


    if (
        !laptop.code ||
        !laptop.model ||
        !laptop.cpu ||
        !laptop.gpu_model ||
        !Number.isFinite(
            laptop.ram
        ) ||
        laptop.ram <= 0 ||
        !Number.isFinite(
            laptop.price
        ) ||
        laptop.price <= 0
    ) {

        alert(
            "Please enter valid laptop data."
        );

        return;

    }


    saveButton.disabled =
        true;


    saveButton.textContent =
        "Adding...";


    try {

        const response =
            await fetch(
                `${API_BASE}/admin/laptops`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify(
                            laptop
                        )
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Failed to add laptop"
            );

        }


        closeModal();


        document
            .getElementById(
                "laptopForm"
            )
            .reset();


        await loadInventory();


        alert(
            "Laptop added successfully ✅"
        );

    }

    catch (error) {

        console.error(error);


        alert(
            "Failed to add laptop ❌\n\n" +
            error.message
        );

    }

    finally {

        saveButton.disabled =
            false;


        saveButton.textContent =
            "Add Laptop";

    }

}


/* =========================
   Events
========================= */

document.addEventListener(
    "DOMContentLoaded",
    () => {

        document
            .getElementById(
                "searchInput"
            )
            .addEventListener(
                "input",
                renderTable
            );


        document
            .getElementById(
                "brandFilter"
            )
            .addEventListener(
                "change",
                renderTable
            );


        document
            .getElementById(
                "sortFilter"
            )
            .addEventListener(
                "change",
                renderTable
            );


        document
            .getElementById(
                "addLaptopBtn"
            )
            .addEventListener(
                "click",
                openModal
            );


        document
            .getElementById(
                "closeModalBtn"
            )
            .addEventListener(
                "click",
                closeModal
            );


        document
            .getElementById(
                "cancelModalBtn"
            )
            .addEventListener(
                "click",
                closeModal
            );


        document
            .getElementById(
                "laptopForm"
            )
            .addEventListener(
                "submit",
                addLaptop
            );


        document
            .getElementById(
                "laptopModal"
            )
            .addEventListener(
                "click",
                event => {

                    if (
                        event.target.id ===
                        "laptopModal"
                    ) {

                        closeModal();

                    }

                }
            );


        loadInventory();

    }
);