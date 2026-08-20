// ================================================================
// Copy / Right-click / DevTools lock
// ================================================================
// Unlock/lock aren't triggered by a modifier shortcut (browsers can
// intercept those) but by typing a plain key sequence anywhere on
// the page: "qqw" unlocks, "ll" re-locks.
const UNLOCK_PATTERN = "qqw";
const LOCK_PATTERN = "ll";
const PATTERN_MAX_LEN = Math.max(UNLOCK_PATTERN.length, LOCK_PATTERN.length);

let isLocked = true;
let keyBuffer = "";

function isEditableTarget(el) {
	return !!el && (el.tagName === "INPUT" || el.tagName === "TEXTAREA" || el.isContentEditable);
}

function isDevToolsShortcut(e) {
	return (
		e.key === "F12" ||
		(e.ctrlKey && e.shiftKey && ["i", "c", "j"].includes(e.key.toLowerCase())) ||
		(e.ctrlKey && e.key.toLowerCase() === "u")
	);
}

document.addEventListener("copy", (e) => {
	if (isLocked) e.preventDefault();
});

document.addEventListener("cut", (e) => {
	if (isLocked) e.preventDefault();
});

document.addEventListener("paste", (e) => {
	if (isLocked) e.preventDefault();
});

document.addEventListener("contextmenu", (e) => {
	if (isLocked) e.preventDefault();
});

document.addEventListener("dragstart", (e) => {
	if (isLocked) e.preventDefault();
});

document.addEventListener("keydown", (e) => {
	// ===================== UNLOCK / LOCK KEY PATTERN =====================
	if (!e.ctrlKey && !e.altKey && !e.metaKey && e.key.length === 1 && !isEditableTarget(e.target)) {
		keyBuffer = (keyBuffer + e.key.toLowerCase()).slice(-PATTERN_MAX_LEN);

		if (keyBuffer.endsWith(UNLOCK_PATTERN)) {
			isLocked = false;
			document.documentElement.classList.add("unlock");
			keyBuffer = "";
		} else if (keyBuffer.endsWith(LOCK_PATTERN)) {
			isLocked = true;
			document.documentElement.classList.remove("unlock");
			keyBuffer = "";
		}
	}

	if (!isLocked) return;

	// Block Ctrl+C and DevTools shortcuts
	if (e.ctrlKey && e.key.toLowerCase() === "c") {
		e.preventDefault();
	}
	if (isDevToolsShortcut(e)) {
		e.preventDefault();
		alert("DevTools access is disabled on this page.");
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
					<div class="logo"><img src="/class/django/pages/assests/logo.ico" alt="Logo" /></div>
					<div>
						<h1>Foxtech</h1>
						<div class="sub"></div>
					</div>
				</div>

				<nav aria-label="Main navigation">
					<ul>
						<li><a href="/class/django/index.html">Home</a></li>
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
