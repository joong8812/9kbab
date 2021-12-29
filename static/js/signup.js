function checkSelectAll()  {
  const checkboxes
      =document.querySelectorAll('input[name="agree"]');
  const checked
      =document.querySelectorAll('input[name="agree"]:checked');
  const selectAll
      =document.querySelector('input[name="selectall"]');

  if(checkboxes.length === checked.length)  {
    selectAll.checked = true;
  }
  else {
    selectAll.checked = false;
  }
}

function selectAll(selectAll)  {
  const checkboxes
      = document.getElementsByName('agree');

  checkboxes.forEach((checkbox) => {
    checkbox.checked = selectAll.checked
  })
}