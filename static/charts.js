// Some predefined globals
var colors = ["#2603e3",  "#ad8478",  "#e575f8",  "#6b99d5",  "#3e1c78",  
              "#306198",  "#5c1de9",  "#b4cf4b",  "#14adc8",  "#ea7308",  
              "#3901f7",  "#039ae8",  "#26f192",  "#f56ae2",  "#6afbf4",  
              "#d55d58",  "#000608",  "#8ee63e",  "#c44ef8",  "#be1247",    
              "#760178",  "#0c9683",  "#e185f8",  "#95537e",  "#184f51",  
              "#de24a8",  "#dc6168",  "#d9ed1b",  "#03e744",  "#fd4b2d"]
var chart

/**
 * Color the datasets
 **/
function color_datasets(datasets){
    for (var i=0; i < datasets.length; i++){
        datasets[i].backgroundColor=colors[i]
    }
    return datasets
}



/**
 * plot a bar chart
 **/
function plot_bar(ctx, data){
	options = {
		barValueSpacing: 20,
        scales: {
            yAxes: [{
                ticks: {
                    min: 0,
                },
            }],
    	},
	}

    chart = new Chart(ctx, {
        type: 'bar',
        data:data,
		options:options,
    })
}


/**
 * plot scatter graph
 **/
function plot_scatter(ctx, datasets){
	chart = new Chart(ctx, {
		type: 'scatter',
		data: {
			datasets: datasets
		},
		options: {
            tooltips:{
                enabled: true,
                callbacks:{
                    label: function(tooltipItem, data){
                        var label = []
                        label.push(data.datasets[tooltipItem.datasetIndex].label)
                        label.push("date: "+ tooltipItem.xLabel)
                        label.push("grade: "+ tooltipItem.yLabel)
                        return label
                    },
                },
            },
            legend: {
                display: false,
            },
            responsive: true,
            scales: {
                xAxes: [{
                    type: 'time',
                    time: {displayFormats: {quarter: 'DD MMM YYYY'}}
                }]
            },
            onClick:  function(evt, item){
                if (!item || !item.length) {return}

                idx = item[0]._datasetIndex
                console.log(datasets[idx])
                //window.location.replace("/");
            }
        },
	});
}


/**
 * Scatter graph data of all submissions from api endpoint
 *
 * label and color the datasets, then plot
 **/
function scatter(ctx, groups, create=false){

    if (!groups || !groups.length){
        // When all groups are unticked, api (graph/resubmissions without ?group= 
        // would return the whole dataset, hack to make an empty graph instead
        chart.data.datasets = []
        chart.update()
        return
    }
    var url = "/graph/resubmissions"
    $.getJSON({url, data:{group:groups}, traditional:true },function(datasets){
        // Color datasets
        datasets = color_datasets(datasets)
        if (create){
            // Clear any previous chart in canvas
            if(chart){chart.destroy()}
            plot_scatter(ctx, datasets)
        }
        else {
            chart.data.datasets = datasets
            chart.update()
        }
    })
}

/**
 * A bar chart of top results for all sumissions.
 * X - student ID
 * X_m - module
 * Y - grade
 **/
function bar(ctx, groups, create=false){
    if (!groups || !groups.length){
        // When all groups are unticked, api (graph/resubmissions without ?group= 
        // would return the whole dataset, hack to make an empty graph instead
        chart.data.datasets = []
        chart.update()
        return
    }
    var url = "/graph/grades"
    $.getJSON({url, data:{group:groups}, traditional:true },function(data){
        data.datasets = color_datasets(data.datasets)
        if (create){
            // Clear any previous chart in canvas
            if(chart){chart.destroy()}
            plot_bar(ctx, data)
        }
        else {
            chart.data = data
            chart.update()
        }
    })

}
