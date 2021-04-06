var isImportanceDescending = false;
var isListNameDescending = false;
var isDeadlineDescending = false;

function sortTable(column, index, isDescending) {
    var table, rows, switching, i, x, y, shouldSwitch;
    table = document.getElementById("myTable");
    switching = true;
    while (switching) {
        switching = false;
        rows = table.rows;
        for (i = 1; i < (rows.length - 1); i++) {
            shouldSwitch = false;
            x = rows[i].getElementsByTagName("td")[index];
            y = rows[i + 1].getElementsByTagName("td")[index];

            if (column == "importanceLevel" && !isDescending){
                if (x.innerHTML > y.innerHTML) {
                    shouldSwitch = true;
                    break;
                }
            } else if (column == "importanceLevel" && isDescending){
                if (x.innerHTML < y.innerHTML) {
                    shouldSwitch = true;
                    break;
                }
            } else if (column == "listName" && !isDescending){
                if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                    shouldSwitch = true;
                    break;
                }
            }  else if (column == "listName" && isDescending){
                if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
                    shouldSwitch = true;
                    break;
                }
            } else if (column == "deadline" && !isDescending){
                if (x.innerHTML > y.innerHTML) {
                    shouldSwitch = true;
                    break;
                }
            } else if (column == "deadline" && isDescending){
                if (x.innerHTML < y.innerHTML) {
                    shouldSwitch = true;
                    break;
                }
            }
        }
        if (shouldSwitch) {
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
        }
    }
}

$("#importanceLevel").click(function() {
    if (isImportanceDescending){
        sortTable("importanceLevel", 1, true);
        isImportanceDescending = false;
    } else {
        sortTable("importanceLevel", 1, false);
        isImportanceDescending = true;
    }
})

$("#listName").click(function() {
    if (isListNameDescending){
        sortTable("listName", 0, true);
        isListNameDescending = false;
    } else {
        sortTable("listName", 0, false);
        isListNameDescending = true;
    }
})

$("#deadline").click(function() {
    if (isDeadlineDescending){
        sortTable("deadline", 2, true);
        isDeadlineDescending = false;
    } else {
        sortTable("deadline", 2, false);
        isDeadlineDescending = true;
    }
})
