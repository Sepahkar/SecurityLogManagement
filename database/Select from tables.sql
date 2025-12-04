Use  [SecurityLogManagement]

Declare @RequestId int = 170
--update ConfigurationChangeRequest_configurationchangerequest set status_code = 'RELMAN' Where Id = @RequestId

Select id,committee_id, committee_user_nationalcode, need_committee, * From ConfigurationChangeRequest_configurationchangerequest Where id = @RequestId

----Update ConfigurationChangeRequest_requesttask set status_code = 'DEFINE' Where request_id = @RequestId

select * from ConfigurationChangeRequest_requesttask Where request_id = @RequestId
Select * From ConfigurationChangeRequest_requesttaskuser RTU
Inner Join ConfigurationChangeRequest_user U
On RTU.user_nationalcode = U.national_code
Where request_task_id in
(select id from ConfigurationChangeRequest_requesttask Where request_id = @RequestId)

--Select * From ConfigurationChangeRequest_datahistory Where record_id = @RequestId
--Order By ID DESC

--select * from ConfigurationChangeRequest_requesttaskuserselected
--Where request_task_user_id in
--(Select Id From ConfigurationChangeRequest_requesttaskuser Where request_task_id in
--(select id from ConfigurationChangeRequest_requesttask Where request_id = @RequestId))


--SELECT TOP (10) *
--  FROM [SecurityLogManagement].[dbo].[ConfigurationChangeRequest_requestflow] Where request_id = @RequestId
--  Order By Id DESC

--SELECT TOP (10) *
--  FROM [SecurityLogManagement].[dbo].[ConfigurationChangeRequest_notificationlog] Where request_id = @RequestId
--  Order By ID DESC


  --Select * From ConfigurationChangeRequest_user Where national_code = '0082628386'