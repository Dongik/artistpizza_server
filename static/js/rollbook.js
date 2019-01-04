const url = 'http://dongik.space/'

var weekNumber = 0

function initView(){
    // current number of week
    var weekNumber = (new Date()).getWeek();
    getRollbooksByWeekNumber(weekNumber)   
}

async function getRollbooksByWeekNumber(weekNumber){
    const response = await fetch(url + 'rollbook');
    const rollbooks = await response.json();
    setRollbooksView(rollbooks)
}

async function getRollbookByDate(date){
    const response = await fetch(url + 'rollbook');
    const myJson = await response.json();
    
}

async function getMemberInfo(memberId){
    const response = await fetch(url + 'rollbook');
    const myJson = await response.json();
}

function getNextWeekRollbook(){
    weekNumber += 1
    getRollbooksByWeekNumber(weekNumber)
}

function getPreviousWeek(){
    weekNumber -= 1
    getRollbooksByWeekNumber(weekNumber)
}

function showMemberInfo(memberId){

}

function setRollbooksView(rollbooks){
    var rollbookTables = []
    container = document.getElementById("rollbooksContainer")
    // container.
    for (rollbook in rollbooks) {
        var table = document.createElement("table")
        
        container.appendChild(table)
    }


}



function setWeekView(rollbooks){

}
