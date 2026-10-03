"use strict";

/* ---------- Config & static UI data ---------- */

const API_BASE = "http://127.0.0.1:8000";

const MAJORS = [
  "Computer Science",
  "Data Science",
  "Engineering",
  "Business",
  "Medicine",
  "Other"
];

const USES = {
  "Programming": ["VS Code", "Git", "Python", "Node.js"],
  "Data Science & AI": ["Jupyter Notebook", "Anaconda", "Python"],
  "Cybersecurity": ["Kali Linux", "Wireshark", "Burp Suite"],
  "Networking & IT": ["Wireshark", "Nmap"],
  "Gaming": ["Steam", "GTA V", "Call of Duty"],
  "Graphic Design": ["Photoshop", "Illustrator", "Figma"],
  "Video Editing": ["Premiere Pro", "After Effects", "DaVinci Resolve"],
  "3D & Rendering": ["Blender", "Maya", "3ds Max"],
  "Engineering": ["MATLAB", "AutoCAD", "SolidWorks"],
  "Architecture": ["AutoCAD", "Revit", "SketchUp"],
  "Business & Analytics": ["Power BI", "Tableau"],
  "Office & Study": ["Microsoft Office"],
  "Content Creation": ["Photoshop", "Premiere Pro"],
  "Cloud & DevOps": ["Docker", "Git"],
  "Embedded Systems": ["Arduino IDE", "MATLAB"]
};

const PREFS = [
  "Performance",
  "Battery Life",
  "Gaming",
  "Portability",
  "Display",
  "Upgradeability"
];

const SW_CATEGORIES = [
  [
    "Development",
    [
      "vs code",
      "pycharm",
      "visual studio",
      "intellij",
      "eclipse",
      "android studio",
      "git",
      "node",
      "python",
      "docker",
      "arduino",
      "stm32",
      "proteus"
    ]
  ],
  [
    "Data",
    [
      "jupyter",
      "anaconda",
      "power bi",
      "tableau",
      "rstudio",
      "r /",
      "sql",
      "postgres",
      "mysql",
      "spark",
      "matlab",
      "excel",
      "access"
    ]
  ],
  [
    "Cybersecurity",
    [
      "kali",
      "wireshark",
      "burp",
      "metasploit",
      "nmap"
    ]
  ],
  [
    "Networking & IT",
    [
      "packet tracer",
      "gns3",
      "eve-ng",
      "vmware",
      "virtualbox",
      "wsl"
    ]
  ],
  [
    "Gaming",
    [
      "steam",
      "epic",
      "fortnite",
      "gta",
      "call of duty",
      "minecraft"
    ]
  ],
  [
    "Design & Media",
    [
      "photoshop",
      "illustrator",
      "indesign",
      "figma",
      "corel",
      "canva",
      "premiere",
      "after effects",
      "davinci",
      "filmora",
      "capcut",
      "blender",
      "maya",
      "3ds",
      "cinema 4d",
      "unreal",
      "unity",
      "obs",
      "fl studio",
      "ableton",
      "audition"
    ]
  ],
  [
    "Engineering & Architecture",
    [
      "autocad",
      "solidworks",
      "catia",
      "ansys",
      "etabs",
      "sap2000",
      "civil 3d",
      "revit",
      "sketchup"
    ]
  ]
];


/* ---------- State ---------- */

const state = {
  step: 0,

  // Step 1
  major: null,

  // Step 2
  uses: new Set(),

  // Step 3
  budget: 30000,

  // Step 4
  software: new Set(),
  allSoftware: [],

  // Step 5
  prefs: new Set()
};

const TOTAL_STEPS = 5;

const $ = (id) => document.getElementById(id);


/* ---------- DOM helpers ---------- */

function el(tag, props = {}, children = []) {

  const node = document.createElement(tag);

  Object.entries(props).forEach(([k, v]) => {

    if (k === "text") {
      node.textContent = v;
    }

    else if (k === "class") {
      node.className = v;
    }

    else {
      node.setAttribute(k, v);
    }

  });

  [].concat(children).forEach((c) => {
    if (c) node.append(c);
  });

  return node;
}


const fmtEGP = (n) =>
  `${Math.round(Number(n)).toLocaleString("en-US")} EGP`;


function show(id) {

  ["hero", "wizard", "loading", "error", "results"]
    .forEach((s) => {
      $(s).hidden = s !== id;
    });

  window.scrollTo({
    top: 0,
    behavior: "smooth"
  });
}


/* ---------- API ---------- */

async function apiGet(path) {

  const res = await fetch(API_BASE + path);

  if (!res.ok) {
    throw new Error(`HTTP ${res.status}`);
  }

  return res.json();
}


async function apiRecommend(payload) {

  let res;

  try {

    res = await fetch(API_BASE + "/recommend", {

      method: "POST",

      headers: {
        "Content-Type": "application/json"
      },

      body: JSON.stringify(payload)

    });

  }

  catch {

    throw {
      title: "Can't reach BUtech",
      msg: "The recommendation service is offline. Start the server and try again."
    };

  }


  if (res.status === 422 || res.status === 400) {

    throw {
      title: "Check your answers",
      msg: "Some of your selections weren't accepted. Review your budget and software, then try again."
    };

  }


  if (!res.ok) {

    throw {
      title: "Something went wrong",
      msg: "We couldn't generate recommendations right now. Please try again."
    };

  }


  let data;

  try {
    data = await res.json();
  }

  catch {
    data = null;
  }


  if (
    !data ||
    !data.results ||
    !Array.isArray(data.results.within_budget) ||
    !Array.isArray(data.results.over_budget)
  ) {

    throw {
      title: "Unexpected response",
      msg: "The service sent data we couldn't read. Please try again."
    };

  }


  return data.results;
}


/* ---------- Software ---------- */

async function loadSoftware() {

  try {

    const data = await apiGet("/software");

    const list = Array.isArray(data)
      ? data
      : data.software || data.available_software || [];

    state.allSoftware = list
      .map((s) => typeof s === "string" ? s : s.name)
      .filter(Boolean);

    renderSoftware();

  }

  catch {

    // Fallback software list

    state.allSoftware = [
      ...new Set(
        Object.values(USES).flat()
      )
    ];

    renderSoftware();

  }

}


/* ---------- Chips ---------- */

function makeChip(label, pressed, onClick) {

  const b = el("button", {

    class: "chip",

    type: "button",

    "aria-pressed": String(pressed),

    text: label

  });


  b.addEventListener("click", () => {

    onClick();

  });


  return b;

}


function renderChips(group, labels, isOn, toggle) {

  const box = document.querySelector(
    `[data-group="${group}"]`
  );

  if (!box) return;


  box.replaceChildren(

    ...labels.map((label) =>

      makeChip(
        label,
        isOn(label),
        () => toggle(label)
      )

    )

  );

}


/* ---------- Step 1: Major ---------- */

function renderMajors() {

  renderChips(

    "major",

    MAJORS,

    (label) => state.major === label,

    (label) => {

      // Major ONLY.
      // It does NOT select uses or software.

      state.major = label;

      renderMajors();

    }

  );

}


/* ---------- Step 2: Uses ---------- */

function renderUses() {

  renderChips(

    "uses",

    Object.keys(USES),

    (label) => state.uses.has(label),

    (label) => {

      if (state.uses.has(label)) {

        state.uses.delete(label);

      }

      else {

        state.uses.add(label);

      }

      renderUses();

    }

  );

}


/* ---------- Step 5: Preferences ---------- */

function renderPrefs() {

  renderChips(

    "prefs",

    PREFS,

    (label) => state.prefs.has(label),

    (label) => {

      if (state.prefs.has(label)) {

        state.prefs.delete(label);

      }

      else {

        state.prefs.add(label);

      }

      renderPrefs();

    }

  );

}


/* ---------- Software ---------- */

function categorize(name) {

  const n = name.toLowerCase();

  const hit = SW_CATEGORIES.find(

    ([, keys]) =>
      keys.some((key) => n.includes(key))

  );

  return hit ? hit[0] : "Other";

}


function renderSoftware() {

  const groups = {};


  state.allSoftware.forEach((software) => {

    const category = categorize(software);

    if (!groups[category]) {
      groups[category] = [];
    }

    groups[category].push(software);

  });


  const order = [

    ...SW_CATEGORIES.map(
      (category) => category[0]
    ),

    "Other"

  ].filter(
    (group) => groups[group]
  );


  const nodes = order.map((group) => {

    const wrap = el(
      "div",
      { class: "sw-group" },
      [
        el("h3", {
          text: group
        })
      ]
    );


    const chips = el(
      "div",
      { class: "chips" }
    );


    groups[group].forEach((software) => {

      chips.append(

        makeChip(

          software,

          state.software.has(software),

          () => {

            if (state.software.has(software)) {

              state.software.delete(software);

            }

            else {

              state.software.add(software);

            }

            renderSoftware();

          }

        )

      );

    });


    wrap.append(chips);

    return wrap;

  });


  $("softwareBox").replaceChildren(

    ...(nodes.length

      ? nodes

      : [
          el(
            "p",
            {
              class: "muted",
              text: "No software available."
            }
          )
        ])

  );

}


/* ---------- Validation ---------- */

function validate(step) {

  if (
    step === 0 &&
    !state.major
  ) {

    return "Choose what you study to continue.";

  }


  if (
    step === 1 &&
    state.uses.size === 0
  ) {

    return "Pick at least one use.";

  }


  if (
    step === 2 &&
    state.budget < 5000
  ) {

    return "Enter a budget of at least 5,000 EGP.";

  }


  if (
    step === 3 &&
    state.software.size === 0
  ) {

    return "Select at least one program you'll run.";

  }


  return "";

}


/* ---------- Wizard Navigation ---------- */

function goTo(step) {

  state.step = step;


  document
    .querySelectorAll(".step")
    .forEach((s) => {

      s.hidden =
        Number(s.dataset.step) !== step;

    });


  $("bar").style.width =
    `${((step + 1) / TOTAL_STEPS) * 100}%`;


  $("stepCount").textContent =
    `Step ${step + 1} of ${TOTAL_STEPS}`;


  document
    .querySelector(".progress")
    .setAttribute(
      "aria-valuenow",
      step + 1
    );


  $("backBtn").style.visibility =
    step === 0
      ? "hidden"
      : "visible";


  $("nextBtn").textContent =
    step === TOTAL_STEPS - 1
      ? "Find my laptop"
      : "Continue";


  $("formError").hidden = true;

}


function next() {

  const err = validate(state.step);


  if (err) {

    $("formError").textContent = err;

    $("formError").hidden = false;

    return;

  }


  if (
    state.step === TOTAL_STEPS - 1
  ) {

    findLaptop();

  }

  else {

    goTo(state.step + 1);

  }

}


/* ---------- Recommendation ---------- */

async function findLaptop() {

  const payload = {

    software: [...state.software],

    budget: state.budget,

    brand: "Any",

    laptop_type: "Any",

    top_n: 5

  };


  show("loading");


  try {

    const results =
      await apiRecommend(payload);

    renderResults(results);

  }

  catch (e) {

    $("errorTitle").textContent =
      e.title || "Something went wrong";

    $("errorMsg").textContent =
      e.msg || "Please try again.";

    show("error");

  }

}


/* ---------- Results ---------- */

function laptopCard(item, alt) {

  const reasons =
    (item.reasons || [])
      .map((reason) =>
        el("li", {
          text: reason
        })
      );


  const specs = el(
    "dl",
    { class: "specs" },
    [

      el("dt", {
        text: "CPU"
      }),

      el("dd", {
        text: item.cpu || "—"
      }),


      el("dt", {
        text: "GPU"
      }),

      el("dd", {
        text: item.gpu_model || "—"
      }),


      el("dt", {
        text: "RAM"
      }),

      el("dd", {

        text:
          item.ram != null

            ? (
                /gb/i.test(item.ram)
                  ? String(item.ram)
                  : `${item.ram} GB`
              )

            : "—"

      })

    ]
  );


  const price = [

    el("div", {
      class: "price",
      text: fmtEGP(item.price)
    })

  ];


  if (
    alt &&
    item.over_budget_amount > 0
  ) {

    price.push(

      el("div", {

        class: "over",

        text:
          `${fmtEGP(item.over_budget_amount)} over budget`

      })

    );

  }


  return el(

    "article",

    {
      class:
        "card" +
        (alt ? " alt" : "")
    },

    [

      el(
        "div",
        { class: "match" },
        [

          el("b", {
            text:
              `${Math.round(item.match_score)}%`
          }),

          el("span", {
            text: "BUtech match"
          })

        ]
      ),


      el("h3", {
        text:
          item.model ||
          item.code
      }),


      el("div", {}, price),


      specs,


      el(
        "ul",
        { class: "reasons" },
        reasons
      )

    ]

  );

}


function renderResults({
  within_budget,
  over_budget
}) {

  const root = $("results");


  const head = el(

    "div",

    { class: "results-head" },

    [

      el(
        "div",
        {},
        [

          el("h2", {
            text: "Your matches"
          }),

          el("p", {
            class: "muted",

            text:
              `Budget: ${fmtEGP(state.budget)}`
          })

        ]
      ),


      el("button", {

        class: "btn ghost",

        id: "editBtn",

        text: "Edit my answers"

      })

    ]

  );


  const nodes = [head];


  if (within_budget.length) {

    nodes.push(

      el("h2", {

        class: "section",

        text: "Within your budget"

      })

    );


    nodes.push(

      el(
        "div",
        { class: "grid" },

        within_budget.map(
          (item) =>
            laptopCard(item, false)
        )

      )

    );

  }

  else {

    nodes.push(

      el("p", {

        class: "muted",

        text:
          "No laptops fit this budget and software mix. Try raising your budget or removing a program."

      })

    );

  }


  if (over_budget.length) {

    nodes.push(

      el("h2", {

        class: "section",

        text: "More powerful options"

      })

    );


    nodes.push(

      el("p", {

        class: "muted",

        text:
          "These go beyond your budget. Shown separately so you can compare."

      })

    );


    nodes.push(

      el(
        "div",
        { class: "grid" },

        over_budget.map(
          (item) =>
            laptopCard(item, true)
        )

      )

    );

  }


  root.replaceChildren(...nodes);


  $("editBtn").addEventListener(
    "click",
    () => show("wizard")
  );


  show("results");

}


/* ---------- Init ---------- */

function init() {

  // Render every step independently.

  renderMajors();

  renderUses();

  renderPrefs();


  const slider =
    $("budget");


  slider.addEventListener(
    "input",
    () => {

      state.budget =
        Number(slider.value);

      $("budgetOut").textContent =
        fmtEGP(state.budget);

    }
  );


  $("startBtn").addEventListener(
    "click",
    () => {

      goTo(0);

      show("wizard");

    }
  );


  $("backBtn").addEventListener(
    "click",
    () =>
      goTo(
        Math.max(
          0,
          state.step - 1
        )
      )
  );


  $("nextBtn").addEventListener(
    "click",
    next
  );


  $("retryBtn").addEventListener(
    "click",
    () =>
      show("wizard")
  );


  loadSoftware();

}


document.addEventListener(
  "DOMContentLoaded",
  init
);