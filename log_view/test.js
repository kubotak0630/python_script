document.write("Hello world JavaScript");

tblElem_ary = document.getElementsByTagName("table");

for (var idx = 0; idx < tblElem_ary.length; idx++) {

  var tbl_ary = [] //要素はrow_ary とすることで2次元配列とする

  //tableデータの値を配列に全部格納する
  for (var i = 0; i < tblElem_ary[idx].rows.length; i++) {
    var row_ary = []
    for (var j = 0; j < tblElem_ary[idx].rows[i].cells.length; j++){
      var cells = tblElem_ary[idx].rows[i].cells[j];
      row_ary.push(cells.firstChild.nodeValue);
    }
    tbl_ary.push(row_ary)
  }
  
  if (tblElem_ary[idx].id == "summary_table"){    
    for (var i = 0; i < tbl_ary.length; i++) {
      if (tbl_ary[i][3] == "NG") {
        tblElem_ary[idx].rows[i].cells[3].style.color = "#EE6557";
        tblElem_ary[idx].rows[i].cells[3].style.fontWeight = "bold";
      }
    }
  }
  else {
    for (var i = 0; i < tbl_ary.length; i++) {
      if (tbl_ary[i][4] != "-" && tbl_ary[i][2] != tbl_ary[i][4]) {
        tblElem_ary[idx].rows[i].style.backgroundColor = "#EE6557";
      }
    }			
  }
}
  