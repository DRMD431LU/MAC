$.noConflict();

function folios_valor() {
  var folio;
  folio = document.getElementById("folio_id").value;
  //console.log(folio);

  document.getElementById("folio2_id").value = folio;
  console.log(document.getElementById("folio2_id").value);
}