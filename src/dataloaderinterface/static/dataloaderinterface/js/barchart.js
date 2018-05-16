/**
 * Created by Mauriel on 5/16/2018.
 */
var c20 = d3.scale.category20();

var margin = {top: 40, right: 20, bottom: 60, left: 60},
    width = $(".svg-container").width() - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

var formatPercent = d3.format(".0%");

var x = d3.scale.ordinal()
    .rangeRoundBands([0, width], .1);

var y = d3.scale.linear()
    .domain([0, 1])
    .range([height, 0]);

var xAxis = d3.svg.axis()
    .scale(x)
    .tickValues([])
    .orient("bottom");

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left")
    .tickFormat(formatPercent);

var tip = d3.tip()
    .attr('class', 'd3-tip')
    .offset([-10, 0])
    .html(function (d) {
        return d.taxon + "<br><br><strong>% of Total Individuals:</strong> <span style='color:red'>" + (d.frequency * 100).toFixed(2) + "%</span>";
    });

var svg = d3.select(".svg-container").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

svg.call(tip);

// Get the data
var data = [];
var total = 0;
$(".taxon").each(function () {
    var name = $(this).find("[data-name]").text().trim();
    var count = parseFloat($(this).find("[data-count]").text().trim());
    data.push({taxon: name, frequency: count});
    total += count;
});

var legendContainer = $("#legend-container table");

// Compute percentages
for (var i = 0; i < data.length; i++) {
    data[i].frequency = data[i].frequency / total;

    // Populate legend container
    legendContainer.append(
        '<tr>' +
            '<td><i style="color: ' + c20(i) + '" class="fa fa-square mdl-list__item-icon" aria-hidden="true"></i></td>'+
            '<td class="mdl-data-table__cell--non-numeric">' +
                data[i].taxon +
            '</td>' +
            '<td>' + (data[i].frequency * 100).toFixed(2) + '%</td>' +
        '</tr>'
    );
}

// Plot the data
x.domain(data.map(function (d) {
    return d.taxon;
}));

svg.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + height + ")")
    .call(xAxis)
    .append("text")
    .attr("class", "label")
    .style("text-anchor", "middle")
    .attr("x", width / 2)
    .attr("y", margin.bottom / 1.5)
    .text("Taxonomic Group");

svg.append("g")
    .attr("class", "y axis")
    .call(yAxis)
    .append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", 6)
    .attr("dy", ".71em")
    .style("text-anchor", "end")
    .text("% of Total Individuals");

svg.selectAll(".bar")
    .data(data)
    .enter().append("rect")
    .attr("class", "bar")
    .attr("x", function (d) {
        return x(d.taxon);
    })
    .attr("width", x.rangeBand())
    .attr("y", function (d) {
        return y(d.frequency);
    })
    .attr("fill", function (d, i) {
        return c20(i);
    })
    .attr("height", function (d) {
        return height - y(d.frequency);
    })
    .on('mouseover', tip.show)
    .on('mouseout', tip.hide);

// Define responsive behavior
function resize() {
    width = $(".svg-container").width() - margin.left - margin.right;

    // Update the range of the scale with new width/height
    x.rangeRoundBands([0, width], .1);

    // Update the axis and text with the new scale
    svg.select(".x.axis")
        .call(xAxis)
        .attr("transform", "translate(0," + height + ")")
        .select(".label")
        .attr("x", width / 2)
        .attr("y", margin.bottom / 1.5);

    svg.select(".y.axis")
        .call(yAxis);

    // Force D3 to recalculate and update the line
    svg.selectAll(".bar")
        .attr("width", x.rangeBand())
        .attr("y", function (d) {
            return y(d.frequency);
        })
        .attr("x", function (d) {
            return x(d.taxon);
        })
        .attr("height", function (d) {
            return height - y(d.frequency);
        })
        .on('mouseover', tip.show)
        .on('mouseout', tip.hide);
};

// Call the resize function whenever a resize event occurs
d3.select(window).on('resize', resize);

// Call the resize function
// resize();

function type(d) {
    d.frequency = +d.frequency;
    return d;
}
