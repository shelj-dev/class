// =====================================================
// CONFIGURATION
// =====================================================

const API_URL = "http://127.0.0.1:8000";

// =====================================================
// STATE
// =====================================================

let currentUser = null;
let entries = [];
let selectedEntryId = null;

// =====================================================
// AUTH UI
// =====================================================

function showRegister() {
	document.getElementById("loginForm").style.display = "none";
	document.getElementById("registerForm").style.display = "block";

	clearMessages();
}

function showLogin() {
	document.getElementById("loginForm").style.display = "block";
	document.getElementById("registerForm").style.display = "none";

	clearMessages();
}

function clearMessages() {
	document.getElementById("authError").textContent = "";
	document.getElementById("authSuccess").textContent = "";
}

// =====================================================
// REGISTER
// =====================================================

async function register() {
	clearMessages();

	const username = document.getElementById("registerUsername").value.trim();

	const email = document.getElementById("registerEmail").value.trim();

	const password = document.getElementById("registerPassword").value;

	if (!username || !email || !password) {
		showError("Please fill all fields.");

		return;
	}

	try {
		const response = await fetch(`${API_URL}/users/create/`, {
			method: "POST",

			headers: {
				"Content-Type": "application/json",
			},

			body: JSON.stringify({
				username: username,
				email: email,
				hashed_password: password,
			}),
		});

		const data = await response.json();

		if (!response.ok) {
			throw new Error(data.detail || "Registration failed");
		}

		document.getElementById("authSuccess").textContent =
			"Account created successfully. Please login.";

		document.getElementById("registerUsername").value = "";
		document.getElementById("registerEmail").value = "";
		document.getElementById("registerPassword").value = "";

		showLogin();
	} catch (error) {
		showError(error.message);
	}
}

// =====================================================
// LOGIN
// =====================================================

async function login() {
	clearMessages();

	const username = document.getElementById("loginUsername").value.trim();

	const password = document.getElementById("loginPassword").value;

	if (!username || !password) {
		showError("Enter username and password.");

		return;
	}

	try {
		const url =
			`${API_URL}/users/login/` +
			`?username=${encodeURIComponent(username)}` +
			`&password=${encodeURIComponent(password)}`;

		const response = await fetch(url, {
			method: "POST",
		});

		const data = await response.json();

		if (!response.ok) {
			throw new Error(data.detail || "Invalid login");
		}

		currentUser = data;

		localStorage.setItem("diaryUser", JSON.stringify(data));

		openDiary();
	} catch (error) {
		showError(error.message);
	}
}

// =====================================================
// OPEN DIARY
// =====================================================

function openDiary() {
	document.getElementById("authPage").style.display = "none";

	document.getElementById("appPage").style.display = "block";

	document.getElementById("currentUsername").textContent = currentUser.username;

	setToday();

	loadEntries();
}

// =====================================================
// LOGOUT
// =====================================================

function logout() {
	currentUser = null;

	localStorage.removeItem("diaryUser");

	document.getElementById("appPage").style.display = "none";

	document.getElementById("authPage").style.display = "flex";

	showLogin();
}

// =====================================================
// LOAD ENTRIES
// =====================================================

async function loadEntries() {
	try {
		const response = await fetch(`${API_URL}/items/`);

		if (!response.ok) {
			throw new Error("Could not load diary entries.");
		}

		entries = await response.json();

		renderEntries();
	} catch (error) {
		console.error(error);

		document.getElementById("entriesList").innerHTML = `<div class="empty">
                    Could not load entries.
                </div>`;
	}
}

// =====================================================
// RENDER ENTRIES
// =====================================================

function renderEntries(filteredEntries = entries) {
	const list = document.getElementById("entriesList");

	list.innerHTML = "";

	if (filteredEntries.length === 0) {
		list.innerHTML = `<div class="empty">
                    No diary entries yet.
                </div>`;

		return;
	}

	// Newest first

	const sorted = [...filteredEntries].sort((a, b) => b.id - a.id);

	sorted.forEach((entry) => {
		let diaryData;

		try {
			diaryData = JSON.parse(entry.data);
		} catch {
			diaryData = {
				content: entry.data,
				date: "",
				mood: "📝",
			};
		}

		const div = document.createElement("div");

		div.className = "entry";

		if (entry.id === selectedEntryId) {
			div.classList.add("active");
		}

		div.innerHTML = `

                <div class="entry-title">

                    ${escapeHTML(entry.title)}

                    ${diaryData.mood || ""}

                </div>

                <div class="entry-date">

                    ${escapeHTML(diaryData.date || "")}

                </div>

                <div class="entry-preview">

                    ${escapeHTML(diaryData.content || "")}

                </div>
            `;

		div.onclick = () => selectEntry(entry.id);

		list.appendChild(div);
	});
}

// =====================================================
// SELECT ENTRY
// =====================================================

function selectEntry(id) {
	const entry = entries.find((item) => item.id === id);

	if (!entry) return;

	selectedEntryId = id;

	let diaryData;

	try {
		diaryData = JSON.parse(entry.data);
	} catch {
		diaryData = {
			content: entry.data,
			date: "",
			mood: "😊",
		};
	}

	document.getElementById("entryTitle").value = entry.title;

	document.getElementById("entryDate").value = diaryData.date || "";

	document.getElementById("entryMood").value = diaryData.mood || "😊";

	document.getElementById("entryContent").value = diaryData.content || "";

	document.getElementById("deleteButton").style.display = "block";

	document.getElementById("saveStatus").textContent = "";

	renderEntries();
}

// =====================================================
// CREATE / UPDATE
// =====================================================

async function saveEntry() {
	const title = document.getElementById("entryTitle").value.trim();

	const date = document.getElementById("entryDate").value;

	const mood = document.getElementById("entryMood").value;

	const content = document.getElementById("entryContent").value.trim();

	if (!title || !content) {
		showStatus("Title and diary content are required.", true);

		return;
	}

	/*
            We store multiple diary properties
            inside the existing String column.

            Example:

            data = {
                date: "...",
                mood: "...",
                content: "..."
            }
        */

	const data = JSON.stringify({
		date: date,

		mood: mood,

		content: content,

		user_id: currentUser.id,

		username: currentUser.username,
	});

	try {
		let response;

		// UPDATE

		if (selectedEntryId !== null) {
			response = await fetch(`${API_URL}/items/${selectedEntryId}`, {
				method: "PUT",

				headers: {
					"Content-Type": "application/json",
				},

				body: JSON.stringify({
					title: title,

					data: data,
				}),
			});
		}

		// CREATE
		else {
			response = await fetch(`${API_URL}/items/`, {
				method: "POST",

				headers: {
					"Content-Type": "application/json",
				},

				body: JSON.stringify({
					title: title,

					data: data,
				}),
			});
		}

		const result = await response.json();

		if (!response.ok) {
			throw new Error(result.detail || "Could not save entry.");
		}

		showStatus(
			selectedEntryId !== null ? "Entry updated successfully." : "Entry saved successfully.",
		);

		await loadEntries();

		// If creating, select newly created entry

		if (selectedEntryId === null) {
			selectedEntryId = result.id;

			renderEntries();
		}

		document.getElementById("deleteButton").style.display = "block";
	} catch (error) {
		showStatus(error.message, true);
	}
}

// =====================================================
// DELETE
// =====================================================

async function deleteEntry() {
	if (selectedEntryId === null) {
		return;
	}

	const confirmDelete = confirm("Delete this diary entry?");

	if (!confirmDelete) {
		return;
	}

	try {
		const response = await fetch(`${API_URL}/items/${selectedEntryId}`, {
			method: "DELETE",
		});

		const result = await response.json();

		if (!response.ok) {
			throw new Error(result.detail || "Could not delete entry.");
		}

		entries = entries.filter((item) => item.id !== selectedEntryId);

		selectedEntryId = null;

		clearEditor();

		renderEntries();

		showStatus("Entry deleted successfully.");
	} catch (error) {
		showStatus(error.message, true);
	}
}

// =====================================================
// NEW ENTRY
// =====================================================

function clearEditor() {
	selectedEntryId = null;

	document.getElementById("entryTitle").value = "";

	setToday();

	document.getElementById("entryMood").value = "😊";

	document.getElementById("entryContent").value = "";

	document.getElementById("deleteButton").style.display = "none";

	document.getElementById("saveStatus").textContent = "";

	renderEntries();
}

// =====================================================
// TODAY
// =====================================================

function setToday() {
	const today = new Date().toISOString().split("T")[0];

	document.getElementById("entryDate").value = today;
}

// =====================================================
// SEARCH
// =====================================================

function searchEntries() {
	const query = document.getElementById("searchInput").value.toLowerCase().trim();

	if (!query) {
		renderEntries();

		return;
	}

	const filtered = entries.filter((entry) => {
		let data;

		try {
			data = JSON.parse(entry.data);
		} catch {
			data = {
				content: entry.data,
			};
		}

		return (
			entry.title.toLowerCase().includes(query) ||
			(data.content || "").toLowerCase().includes(query)
		);
	});

	renderEntries(filtered);
}

// =====================================================
// STATUS
// =====================================================

function showStatus(message, isError = false) {
	const status = document.getElementById("saveStatus");

	status.textContent = message;

	status.style.color = isError ? "#d93025" : "#188038";
}

function showError(message) {
	document.getElementById("authError").textContent = message;
}

// =====================================================
// HTML ESCAPE
// =====================================================

function escapeHTML(value) {
	const div = document.createElement("div");

	div.textContent = value ?? "";

	return div.innerHTML;
}

// =====================================================
// RESTORE LOGIN
// =====================================================

window.addEventListener("DOMContentLoaded", () => {
	const savedUser = localStorage.getItem("diaryUser");

	if (savedUser) {
		try {
			currentUser = JSON.parse(savedUser);

			openDiary();
		} catch {
			localStorage.removeItem("diaryUser");
		}
	}
});
