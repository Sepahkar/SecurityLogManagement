Declare @RequestId int = 152
Select committee_id, committee_user_nationalcode, need_committee, * From ConfigurationChangeRequest_configurationchangerequest Where id = @RequestId
--update ConfigurationChangeRequest_configurationchangerequest set committee_id = 3 where id = 143
select * from ConfigurationChangeRequest_requesttask Where request_id = @RequestId

Select * From ConfigurationChangeRequest_datahistory Where record_id = @RequestId
Order By ID DESC

SELECT TOP (10) *
  FROM [SecurityLogManagement].[dbo].[ConfigurationChangeRequest_requestflow] Where request_id = @RequestId
  Order By Id DESC

SELECT TOP (10) *
  FROM [SecurityLogManagement].[dbo].[ConfigurationChangeRequest_notificationlog] Where request_id = @RequestId
  Order By ID DESC