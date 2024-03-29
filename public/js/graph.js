var colors = d3.scaleOrdinal(d3.schemeCategory10);

var svg = d3.select("svg"),
    width = +svg.attr("width"),
    height = +svg.attr("height"),
    node,
    link;

svg.append('defs').append('marker')
    .attrs({
        'id': 'arrowhead',
        'viewBox': '0 0 10 10',
        'refX': 25,
        'refY': 0,
        'orient': 'auto',
        'markerWidth': 13,
        'markerHeight': 13,
        'xoverflow': 'visible'
    })
    .append('svg:path')
    .attr('d', 'M 0,-5 L 10 ,0 L 0,5')
    .attr('fill', '#999')
    .style('stroke', 'none');

var simulation = d3.forceSimulation()
    .force("link", d3.forceLink().id(function (d) { return d.id; }).distance(300).strength(1))
    .force("charge", d3.forceManyBody())
    .force("center", d3.forceCenter(width / 2, height / 2));


// TEST json data in a variable
//var graphtext = '{"nodes": [{"name": "URL","label": " http://www.espn.com","id": 1},{"name": "URL","label": " http://twitter.com/intent/tweet?url=http%3A%2f%2fwww.espn.com%2fespn%2ffeature%2fstory%2f_%2fid%2f18332398%2fespn%2dfantasy%2dapp%2despn&text=Download+the+ESPN+Fantasy+App","id": 2},{"name": "URL","label": " https://twitter.com/signup?context=webintent","id": 3},{"name": "URL","label": " https://twitter.com/signup?context=webintent","id": 4}],"links": [{"source": 1,"target": 2,"type": "Links_To"},{"source": 2,"target": 3,"type": "Links_To"},{"source": 3,"target": 4,"type": "Links_To"}]}';

//  TEST Create a cookie test using the variable
//$.cookie('graph_session', graphtext);

// TEST JSON data is good
//console.log($.cookie('graph_session'));

//If the cookie exists load the graph
if ($.cookie('graph_session')) {

    if (localStorage.getItem("localGraph") === null) {
        // read json from file into a variable

        //var jsonObject = $.getJSON("graphFile.json");
        function ajax1() {
            return $.ajax({
                type: "GET",
                url: "graphFile.json",
                dataType: "json",
            });


        }
        $.when(ajax1()).done(function (a1) {
            jsonobj = JSON.stringify(a1);
            //console.log("jsonObject-After" + jsonobj);

            //write data from file to local storage
            localStorage.setItem("localGraph", jsonobj);

            // get json file from local storage to a variable
            var retrieved = localStorage.getItem("localGraph");
            //console.log("retrieved: " + retrieved);

            // Parse nodes and links from json file
            graphjson = JSON.parse(retrieved);
            // Send the parsed json data to the graph update function
            update(graphjson.links, graphjson.nodes);
        });
    }
    else {
        var retrieved = localStorage.getItem("localGraph");
        console.log("Else retrieved: " + retrieved);
        // Parse nodes and links from json file
        graphjson = JSON.parse(retrieved);
        // Send the parsed json data to the graph update function
        update(graphjson.links, graphjson.nodes);
    }
}
else {
    console.log("No Cookie found")
}


function update(links, nodes) {
    link = svg.selectAll(".link")
        .data(links)
        .enter()
        .append("line")
        .attr("class", "link")
        .attr('marker-end', 'url(#arrowhead)')
    link.append("title")
        .text(function (d) { return d.type; });
    edgepaths = svg.selectAll(".edgepath")
        .data(links)
        .enter()
        .append('path')
        .attrs({
            'class': 'edgepath',
            'fill-opacity': 0,
            'stroke-opacity': 0,
            'id': function (d, i) { return 'edgepath' + i }
        })
        .style("pointer-events", "none");
    edgelabels = svg.selectAll(".edgelabel")
        .data(links)
        .enter()
        .append('text')
        .style("pointer-events", "none")
        .attrs({
            'class': 'edgelabel',
            'id': function (d, i) { return 'edgelabel' + i },
            'font-size': 10,
            'fill': '#aaa'
        });
    edgelabels.append('textPath')
        .attr('xlink:href', function (d, i) { return '#edgepath' + i })
        .style("text-anchor", "middle")
        .style("pointer-events", "none")
        .attr("startOffset", "50%")
        .text(function (d) { return d.type });
    node = svg.selectAll(".node")
        .data(nodes)
        .enter()
        .append("g")
        .attr("class", "node")
        .call(d3.drag()
            .on("start", dragstarted)
            .on("drag", dragged)
        );
    node.append("circle")
        .attr("r", 20)
        .style("fill", function (d, i) { return colors(i); })
    node.append("title")
        .text(function (d) { return d.id; });
    node.append("text")
        .attr("dy", -3)
        .text(function (d) { return d.name + ":" + d.label; });
    simulation
        .nodes(nodes)
        .on("tick", ticked);
    simulation.force("link")
        .links(links);
}

function ticked() {
    link
        .attr("x1", function (d) { return d.source.x; })
        .attr("y1", function (d) { return d.source.y; })
        .attr("x2", function (d) { return d.target.x; })
        .attr("y2", function (d) { return d.target.y; });
    node
        .attr("transform", function (d) { return "translate(" + d.x + ", " + d.y + ")"; });
    edgepaths.attr('d', function (d) {
        return 'M ' + d.source.x + ' ' + d.source.y + ' L ' + d.target.x  + ' ' + d.target.y;
    });
    edgelabels.attr('transform', function (d) {
        if (d.target.x < d.source.x) {
            var bbox = this.getBBox();
            rx = bbox.x + bbox.width / 2;
            ry = bbox.y + bbox.height / 2;
            return 'rotate(180 ' + rx + ' ' + ry + ')';
        }
        else {
            return 'rotate(0)';
        }
    });
}

function dragstarted(d) {
    if (!d3.event.active) simulation.alphaTarget(0.3).restart()
    d.fx = d.x;
    d.fy = d.y;
}

function dragged(d) {
    d.fx = d3.event.x;
    d.fy = d3.event.y;
}