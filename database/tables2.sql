Use SecurityLogManagement

Declare @RequestId int = 174
Declare @TaskId int = 590

Select * From [dbo].[ConfigurationChangeRequest_configurationchangerequest]
Where id = @RequestId


Select cv.Caption as user_opinion,rf.* From ConfigurationChangeRequest_requestflow rf
inner join ConfigurationChangeRequest_constvalue cv
on rf.user_opinion_id = cv.id
Where request_id = @RequestId
order by id desc

select * from ConfigurationChangeRequest_requesttask
where request_id = @RequestId

select rtu.*, u.first_name + ' ' + u.last_name from ConfigurationChangeRequest_requesttaskuser rtu
inner join ConfigurationChangeRequest_user u
on rtu.user_nationalcode = u.national_code
Where request_task_id in
(select id from ConfigurationChangeRequest_requesttask
where request_id = @RequestId and (request_task_id = @TaskId or @TaskId = -1)
)
order by request_task_id, user_role_code


select rtus.*,  u.first_name + ' ' + u.last_name from ConfigurationChangeRequest_requesttaskuserselected rtus
inner join ConfigurationChangeRequest_requesttaskuser rtu
on rtus.request_task_user_id = rtu.id
inner join ConfigurationChangeRequest_user u
on rtu.user_nationalcode = u.national_code
Where request_task_user_id in
(Select id From ConfigurationChangeRequest_requesttaskuser Where request_task_id in
(select id from ConfigurationChangeRequest_requesttask
where request_id = @RequestId and (request_task_id = @TaskId or @TaskId = -1)
))

select * from ConfigurationChangeRequest_notificationlog
Where variables like N'%ConfigurationChangeRequest/'+CAST(@RequestId as varchar(10))+'%' or 
variables like N'%ConfigurationChangeRequest/task/'+CAST(@TaskId as varchar(10))+'%' 
