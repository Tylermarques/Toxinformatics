var columns = [
    {title: "Name", field: "target_name", frozen:true},
    {title: "PFam", field: "PFam"},
    {title: "Full Sequence E-Value", field: "fs_E-value"},
    {title: "Best Domain E-Value", field: "bd_E-value"},
    {title: "Target Description", field: "description_of_target"},
];

var table = new Tabulator("#table-holder", {
    tooltipGenerationMode: "hover",
    tooltips: function (cell) {
        return cell.getValue()
    },
    height: window.innerHeight * 0.8, // set height of table (in CSS or here), this enables the Virtual DOM and improves render speed dramatically (can be any valid css height value)
    data: tabledata, //assign data to table
    layout: "fitColumns", //fit columns to width of table (optional)
    columns: columns,
    rowClick: function (e, row) { //trigger an alert message when the row is clicked
            window.open('http://pfam.xfam.org/family/' + row.getData().PFam )

    },
});
$("#download-csv").click(function () {
    table.download("csv", "data.csv");
});