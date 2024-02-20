const stepCheckbox = document.getElementById("step-checkbox");
const xMinInput = document.getElementById("xmin-input");
const xMaxInput = document.getElementById("xmax-input");

xMinInput.addEventListener("change", () => {
  if (
    stepCheckbox.checked &&
    parseInt(xMaxInput.value) - parseInt(xMinInput.value) >= 10
  ) {
    xMaxInput.value = -parseInt(xMinInput.value);
  } else if (
    stepCheckbox.checked &&
    parseInt(xMaxInput.value) - parseInt(xMinInput.value) < 10
  ) {
    xMaxInput.value = parseInt(xMinInput.value) + 10;
  }
});

xMaxInput.addEventListener("change", () => {
  if (
    stepCheckbox.checked &&
    parseInt(xMaxInput.value) - parseInt(xMinInput.value) >= 10
  ) {
    xMinInput.value = -parseInt(xMaxInput.value);
  } else if (
    stepCheckbox.checked &&
    parseInt(xMaxInput.value) - parseInt(xMinInput.value) < 10
  ) {
    xMaxInput.value = parseInt(xMinInput.value) + 10;
  }
});

stepCheckbox.addEventListener("change", () => {
  if (stepCheckbox.checked) {
    xMinInput.step = 5;
    xMaxInput.step = 5;
  } else {
    xMinInput.step = 1;
    xMaxInput.step = 1;
  }
});
