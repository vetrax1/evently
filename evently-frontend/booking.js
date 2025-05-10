// evently-frontend/booking.js

const API_URL = "http://localhost:5000/api";

async function fetchEvents() {
  const res = await fetch(`${API_URL}/events`);
  const events = await res.json();
  const container = document.getElementById("events");

  events.forEach((event) => {
    const card = document.createElement("div");
    card.className = "bg-white p-4 rounded shadow hover:shadow-md transition";

    card.innerHTML = `
      <h4 class="text-lg font-bold mb-1">${event.title}</h4>
      <p class="text-sm text-gray-600 mb-1"><strong>Location:</strong> ${event.location}</p>
      <p class="text-sm text-gray-600 mb-1"><strong>Date:</strong> ${event.date}</p>
      <p class="text-sm text-gray-600 mb-3"><strong>Seats Left:</strong> ${event.remaining_seats}</p>
      <button onclick="openModal(${event.id}, '${event.title}')" class="w-full bg-blue-700 text-white p-2 rounded hover:bg-blue-800">Book Now</button>
    `;

    container.appendChild(card);
  });
}

function openModal(id, title) {
  document.getElementById("modal").classList.remove("hidden");
  document.getElementById("modal-title").textContent = `Book: ${title}`;
  document.getElementById("event-id").value = id;
}

function closeModal() {
  document.getElementById("modal").classList.add("hidden");
}

function showToast(message = "Success!") {
  const toast = document.getElementById("toast");
  toast.textContent = message;
  toast.classList.remove("hidden");
  setTimeout(() => toast.classList.add("hidden"), 3000);
}

// Booking logic
document.getElementById("booking-form").addEventListener("submit", async (e) => {
  e.preventDefault();

  const id = document.getElementById("event-id").value;
  const name = document.getElementById("name").value;
  const email = document.getElementById("email").value;

  const res = await fetch(`${API_URL}/book/${id}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, email }),
  });

  if (res.ok) {
    showToast("🎉 Booking successful!");
    closeModal();
    document.getElementById("booking-form").reset();
  } else {
    const error = await res.json();
    showToast(`❌ ${error.error || "Booking failed."}`);
  }
});

function scrollToEvents() {
  document.getElementById("events-section").scrollIntoView({ behavior: "smooth" });
}

fetchEvents();
