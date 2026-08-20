const UNLOCK_PASSWORD = "shelji";
const UNLOCK_KEYS = {
	ctrl: true,
	alt: false,
	key: "p",
	l_key: "l",
};
// let isLocked = true;
let isLocked = false;

document.addEventListener("copy", (e) => {
	if (isLocked) e.preventDefault();
});

document.addEventListener("contextmenu", (e) => {
	if (isLocked) e.preventDefault();
});

document.addEventListener("keydown", (e) => {
	// Block Ctrl+C
	if (isLocked) {
		if (e.ctrlKey && e.key.toLowerCase() === "c") e.preventDefault();
		if (
			e.key === "F12" ||
			(e.ctrlKey && e.shiftKey && ["i", "c", "j"].includes(e.key.toLowerCase())) ||
			(e.ctrlKey && e.key.toLowerCase() === "u")
		) {
			e.preventDefault();
			alert("NO NO GO AND TYPE YOUR CODE😒😒🤐🤡");
		}
	}
	// Block DevTools shortcuts
	if (
		isLocked &&
		(e.key === "F12" ||
			(e.ctrlKey && e.shiftKey && ["i", "c", "j"].includes(e.key.toLowerCase())) ||
			(e.ctrlKey && e.key.toLowerCase() === "u"))
	) {
		e.preventDefault();
		alert("NO NO GO AND TYPE YOUR CODE😒😒🤐🤡");
	}

	// ===================== UNLOCK SHORTCUT =====================
	if (
		e.ctrlKey === UNLOCK_KEYS.ctrl &&
		e.altKey === UNLOCK_KEYS.alt &&
		e.key.toLowerCase() === UNLOCK_KEYS.key
	) {
		e.preventDefault();
		// const pass = prompt("Enter unlock password:");
		const pass = "shelj";

		if (pass === UNLOCK_PASSWORD) { 
			isLocked = false;
			document.documentElement.classList.add("unlock");
			// alert("😎");
		} else {
			alert("😅");
		}
	}
	if (
		e.ctrlKey === UNLOCK_KEYS.ctrl &&
		e.altKey === UNLOCK_KEYS.alt &&
		e.key.toLowerCase() === UNLOCK_KEYS.l_key
	) {
		isLocked = true;
		document.documentElement.classList.remove("unlock");
		// alert("😁");
	}
});

// Images navigations
const images = document.querySelectorAll(".gallery-img");
const lightbox = document.getElementById("lightbox");
const lightboxImg = document.getElementById("lightbox-img");
const closeBtn = document.getElementById("close");
const prevBtn = document.getElementById("prev");
const nextBtn = document.getElementById("next");

let currentIndex = 0;

images.forEach((img, index) => {
	img.addEventListener("click", () => {
		currentIndex = index;
		showImage();
		lightbox.style.display = "flex";
	});
});

function showImage() {
	lightboxImg.src = images[currentIndex].src;
}

prevBtn.onclick = () => {
	currentIndex = (currentIndex - 1 + images.length) % images.length;
	showImage();
};

nextBtn.onclick = () => {
	currentIndex = (currentIndex + 1) % images.length;
	showImage();
};

closeBtn.onclick = () => (lightbox.style.display = "none");

lightbox.addEventListener("click", (e) => {
	if (e.target === lightbox) lightbox.style.display = "none";
});

document.addEventListener("keyup", (e) => {
	if (e.key === "Escape") {
		lightbox.style.display = "none";
	}
});
// --------------------------------------------------------------
// Navbar
const headerData = `<div class="brand">
					<div class="logo"><img src="pages/assests/logo.ico" alt="Logo q" /></div>
					<div>
						<h1>Foxtech</h1>
						<div class="sub"></div>
					</div>
				</div>

				<nav aria-label="Main navigation">
					<ul>
						<li><a href="/django/index.html">Home</a></li>
					</ul>
				</nav>`;
const header = document.getElementById("header");

header.innerHTML = headerData;

// --------------------------------------------------------------
// Footer
const footerData = `<footer style="background:#222; color:#fff; padding:15px; text-align:center; margin-top:40px;">
    <p>&copy; 2026 Foxtech Private Solutions</p>
    <p>
		<h3 style="display: inline-block">Contributors: </h3>
        <a href="#" style="color:#ccc; text-decoration:none;">Foxtech.dev.labs</a>
    </p>
</footer>
`;
const footer = document.getElementById("footer");

footer.innerHTML = footerData;

// --------------------------------------------------------------
