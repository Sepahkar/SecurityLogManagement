$('.task-table tbody tr').click(function()
{
        task_id = $(this).data('task-id')
        console.log('taskid = ' + task_id)
        console.log( window.location.origin + '/ConfigurationChangeRequest/task/' + task_id)
        debugger
        window.location.href = window.location.origin + '/ConfigurationChangeRequest/task/' + task_id

})