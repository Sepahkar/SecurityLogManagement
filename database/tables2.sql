Declare @RequestId int = 171

Select * From [dbo].[ConfigurationChangeRequest_configurationchangerequest]
Where id = @RequestId


Select * From ConfigurationChangeRequest_requestflow
Where request_id = @RequestId

select * from ConfigurationChangeRequest_requesttask
where request_id = @RequestId

select * from ConfigurationChangeRequest_requesttaskuserselected
Where request_task_user_id in
(Select id From ConfigurationChangeRequest_requesttaskuser Where request_task_id in
(select id from ConfigurationChangeRequest_requesttask
where request_id = @RequestId
))