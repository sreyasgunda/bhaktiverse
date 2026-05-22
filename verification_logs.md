
--- 1∩╕ÅΓâú Scenario 1: Daily Assigned Service Mail Test ---
================================================================================
      BHAKTIVERSE REAL END-TO-END EXECUTION TEST SUITE
================================================================================

--- [1] Scheduler Execution Verification ---
   [REGISTERED] job_id='scan_seva_job', function='scan_seva_duties'
   [REGISTERED] job_id='scan_sadhana_job', function='scan_sadhana_entries'
   [REGISTERED] job_id='scan_inactive_job', function='scan_inactive_devotees'
   [REGISTERED] job_id='daily_assignment_job', function='send_daily_assignment_emails'
   [STATUS] APScheduler/BackgroundScheduler initialized successfully!
BhaktiVerse Scheduler Started
   [PASS]: All scheduler jobs are successfully registered and executing.

--- [2] Timezone Verification ---
   * settings.TIME_ZONE    : UTC
   * timezone.now()        : 2026-05-21 11:40:29.220162+00:00
   * timezone.localtime()  : 2026-05-21 11:40:29.220216+00:00
   [PASS]: timezone.now() is timezone-aware.

[DB SETUP] Cleaning database tables for verification...
   [USERS CREATED]
      - Leader: temple_leader_test@bhaktiverse.com (Residency: Mayapur Residency)
      - Devotee 1: devotee_test1@bhaktiverse.com (Residency: Mayapur Residency)
      - Devotee 2: devotee_test2@bhaktiverse.com (Residency: Mayapur Residency)
EMAIL SENT ΓåÆ Daily Seva Assignment
   Creating a 7-day Weekly Seva Assignment for Devotee Ramananda (from 2026-05-22 to 2026-05-28)
   Total DailySeva records generated: 7
   Verifying devotees DO NOT receive all 7 emails immediately:
      Emails sent immediately on creation: 0

   [SIMULATING DAY 1: 8:00 AM]
   [BEFORE DAY 1 RUN] ID: 181 | service_name: 'Morning Deity Altar Worship'
      * assignment_email_sent : False
      * reminder_30_sent       : False
      * reminder_start_sent    : False
      * last_reminder_time     : None
      * overdue_alert_sent     : False
      * status                 : 'pending'
      * completed              : False
EMAIL SENT ΓåÆ Daily Seva Assignment
   [AFTER DAY 1 RUN] ID: 181 | service_name: 'Morning Deity Altar Worship'
      * assignment_email_sent : True
      * reminder_30_sent       : False
      * reminder_start_sent    : False
      * last_reminder_time     : None
      * overdue_alert_sent     : False
      * status                 : 'pending'
      * completed              : False
      [EMAIL #1]
         Subject: New Service Assigned
         To: ['devotee_test1@bhaktiverse.com']
         Body Snippet: You have been assigned the service: Morning Deity Altar Worship

   [SIMULATING DAY 1 REPEATED RUN TO CONFIRM DUPLICATE PREVENTION]
      Duplicate emails triggered: 0

   [SIMULATING DAY 2 (TOMORROW): 8:00 AM]
   [BEFORE DAY 2 RUN] ID: 182 | service_name: 'Morning Deity Altar Worship'
      * assignment_email_sent : False
      * reminder_30_sent       : False
      * reminder_start_sent    : False
      * last_reminder_time     : None
      * overdue_alert_sent     : False
      * status                 : 'pending'
      * completed              : False
   Γ£à Scenario 1 Status: PASS
   [AFTER DAY 2 RUN] ID: 182 | service_name: 'Morning Deity Altar Worship'
      * assignment_email_sent : True
      * reminder_30_sent       : False
      * reminder_start_sent    : False
      * last_reminder_time     : None
      * overdue_alert_sent     : False
      * status                 : 'pending'
      * completed              : False
      [EMAIL #1]
         Subject: New Service Assigned
         To: ['devotee_test1@bhaktiverse.com']
         Body Snippet: You have been assigned the service: Morning Deity Altar Worship

--- 2∩╕ÅΓâú Scenario 2: 10-Min Reminder Flow Test ---
SCHEDULER RUNNING ΓåÆ scan_seva_duties
   Creating Seva: 'Afternoon Prasad Distribution' (10:00 AM - 10:30 AM, Duration: 30m)

   [SIMULATING 9:30 AM - 30 Min Reminder]
   [BEFORE 9:30 SCAN] ID: 188 | service_name: 'Afternoon Prasad Distribution'
      * assignment_email_sent : False
      * reminder_30_sent       : False
      * reminder_start_sent    : False
      * last_reminder_time     : None
      * overdue_alert_sent     : False
      * status                 : 'pending'
      * completed              : False
EMAIL SENT ΓåÆ 30 min reminder
SCHEDULER RUNNING ΓåÆ scan_seva_duties
   [AFTER 9:30 SCAN] ID: 188 | service_name: 'Afternoon Prasad Distribution'
      * assignment_email_sent : False
      * reminder_30_sent       : True
      * reminder_start_sent    : False
      * last_reminder_time     : None
      * overdue_alert_sent     : False
      * status                 : 'pending'
      * completed              : False
      [EMAIL #1]
         Subject: Seva Reminder
         To: ['devotee_test1@bhaktiverse.com']
         Body Snippet: Your service starts in 30 minutes.

   [SIMULATING 10:00 AM - Start Time Reminder]
   [BEFORE 10:00 SCAN] ID: 188 | service_name: 'Afternoon Prasad Distribution'
      * assignment_email_sent : False
      * reminder_30_sent       : True
      * reminder_start_sent    : False
      * last_reminder_time     : None
      * overdue_alert_sent     : False
      * status                 : 'pending'
      * completed              : False
EMAIL SENT ΓåÆ Service start reminder
SCHEDULER RUNNING ΓåÆ scan_seva_duties
   [AFTER 10:00 SCAN] ID: 188 | service_name: 'Afternoon Prasad Distribution'
      * assignment_email_sent : False
      * reminder_30_sent       : True
      * reminder_start_sent    : True
      * last_reminder_time     : 2026-05-22 10:00:00+00:00
      * overdue_alert_sent     : False
      * status                 : 'pending'
      * completed              : False
      [EMAIL #1]
         Subject: Seva Started
         To: ['devotee_test1@bhaktiverse.com']
         Body Snippet: Your service time has started.

   [SIMULATING 10:10 AM - 10 Min Reminder #1]
   [BEFORE 10:10 SCAN] ID: 188 | service_name: 'Afternoon Prasad Distribution'
      * assignment_email_sent : False
      * reminder_30_sent       : True
      * reminder_start_sent    : True
      * last_reminder_time     : 2026-05-22 10:00:00+00:00
      * overdue_alert_sent     : False
      * status                 : 'pending'
      * completed              : False
EMAIL SENT ΓåÆ 10 min reminder
SCHEDULER RUNNING ΓåÆ scan_seva_duties
   [AFTER 10:10 SCAN] ID: 188 | service_name: 'Afternoon Prasad Distribution'
      * assignment_email_sent : False
      * reminder_30_sent       : True
      * reminder_start_sent    : True
      * last_reminder_time     : 2026-05-22 10:10:00+00:00
      * overdue_alert_sent     : False
      * status                 : 'pending'
      * completed              : False
      [EMAIL #1]
         Subject: Seva Reminder
         To: ['devotee_test1@bhaktiverse.com']
         Body Snippet: Please remember to complete your ongoing service.

   [SIMULATING DEVOTEE MARKING SEVA COMPLETED AT 10:12 AM]
   [POST-COMPLETION] ID: 188 | service_name: 'Afternoon Prasad Distribution'
      * assignment_email_sent : False
      * reminder_30_sent       : True
      * reminder_start_sent    : True
      * last_reminder_time     : 2026-05-22 10:10:00+00:00
      * overdue_alert_sent     : False
      * status                 : 'completed'
      * completed              : True

   [SIMULATING 10:20 AM - scan (should trigger 0 emails due to completion)]
SCHEDULER RUNNING ΓåÆ scan_seva_duties
      (No emails triggered)

   [SIMULATING 10:30 AM - scan (should trigger 0 overdue alerts)]
   Γ£à Scenario 2 Status: PASS
      (No emails triggered)
Debug: pass_s2_930=True (1 emails), pass_s2_1000=True (1 emails), pass_s2_1010=True (1 emails), pass_s2_1020=True (0 emails), pass_s2_1030=True (0 emails)

--- 3∩╕ÅΓâú Scenario 3: Overdue Failure Alert Test ---
SCHEDULER RUNNING ΓåÆ scan_seva_duties
   Creating Seva: 'Temple Cleaning' (11:00 AM - 11:30 AM, Duration: 30m)

   [SIMULATING 11:30 AM - Duration ends, Seva not completed]
   [BEFORE SCAN] ID: 189 | service_name: 'Temple Cleaning'
      * assignment_email_sent : False
      * reminder_30_sent       : False
      * reminder_start_sent    : False
      * last_reminder_time     : None
      * overdue_alert_sent     : False
      * status                 : 'pending'
      * completed              : False
EMAIL SENT ΓåÆ Service not completed alert
SCHEDULER RUNNING ΓåÆ scan_seva_duties
   [AFTER SCAN] ID: 189 | service_name: 'Temple Cleaning'
      * assignment_email_sent : False
      * reminder_30_sent       : False
      * reminder_start_sent    : False
      * last_reminder_time     : None
      * overdue_alert_sent     : True
      * status                 : 'pending'
      * completed              : False
      [EMAIL #1]
         Subject: Service Not Completed
         To: ['temple_leader_test@bhaktiverse.com']
         Body Snippet: Devotee did not complete assigned seva on time.

   [SIMULATING 11:31 AM - Duplicate Overdue Prevention Check]

--- 4∩╕ÅΓâú Scenario 4: Sadhana Reminder System Test ---
   Duplicate overdue emails: 0
   [PASS]: Overdue alert sent to leaders. Duplicate prevented successfully.
EMAIL SENT ΓåÆ 8 AM sadhana reminder

   [SIMULATING 8:00 AM - Japa Reminder #1]
EMAIL SENT ΓåÆ 8 AM sadhana reminder
EMAIL SENT ΓåÆ 8 AM sadhana reminder
EMAIL SENT ΓåÆ 8 AM sadhana reminder
EMAIL SENT ΓåÆ 8 AM sadhana reminder
EMAIL SENT ΓåÆ 8 AM sadhana reminder
      [EMAIL #1]
         Subject: Reminder: Submit Daily Sadhana
         To: ['devotee@example.com']
         Body Snippet: Hare Krishna! Please submit your daily sadhana entry on the BhaktiVerse Devotee Dashboard.
      [EMAIL #2]
         Subject: Reminder: Submit Daily Sadhana
         To: ['devotee_4005@example.com']
         Body Snippet: Hare Krishna! Please submit your daily sadhana entry on the BhaktiVerse Devotee Dashboard.
      [EMAIL #3]
         Subject: Reminder: Submit Daily Sadhana
         To: ['gsreyaskumar_cse235a0510@mgit.ac.in']
         Body Snippet: Hare Krishna! Please submit your daily sadhana entry on the BhaktiVerse Devotee Dashboard.
      [EMAIL #4]
         Subject: Reminder: Submit Daily Sadhana
         To: ['devotee_test1@bhaktiverse.com']
         Body Snippet: Hare Krishna! Please submit your daily sadhana entry on the BhaktiVerse Devotee Dashboard.
      [EMAIL #5]
         Subject: Reminder: Submit Daily Sadhana
         To: ['devotee_test2@bhaktiverse.com']
         Body Snippet: Hare Krishna! Please submit your daily sadhana entry on the BhaktiVerse Devotee Dashboard.
      Duplicate 8:00 AM reminders: 0

   [SIMULATING 9:00 AM - Japa Reminder #2]
EMAIL SENT ΓåÆ 8 AM sadhana reminder
EMAIL SENT ΓåÆ 8 AM sadhana reminder
EMAIL SENT ΓåÆ 8 AM sadhana reminder
EMAIL SENT ΓåÆ 8 AM sadhana reminder
EMAIL SENT ΓåÆ 8 AM sadhana reminder
      [EMAIL #1]
         Subject: Reminder: Submit Daily Sadhana
         To: ['devotee@example.com']
         Body Snippet: Hare Krishna! Please submit your daily sadhana entry on the BhaktiVerse Devotee Dashboard.
      [EMAIL #2]
         Subject: Reminder: Submit Daily Sadhana
         To: ['devotee_4005@example.com']
         Body Snippet: Hare Krishna! Please submit your daily sadhana entry on the BhaktiVerse Devotee Dashboard.
      [EMAIL #3]
         Subject: Reminder: Submit Daily Sadhana
         To: ['gsreyaskumar_cse235a0510@mgit.ac.in']
         Body Snippet: Hare Krishna! Please submit your daily sadhana entry on the BhaktiVerse Devotee Dashboard.
      [EMAIL #4]
         Subject: Reminder: Submit Daily Sadhana
         To: ['devotee_test1@bhaktiverse.com']
         Body Snippet: Hare Krishna! Please submit your daily sadhana entry on the BhaktiVerse Devotee Dashboard.
      [EMAIL #5]
         Subject: Reminder: Submit Daily Sadhana
         To: ['devotee_test2@bhaktiverse.com']
         Body Snippet: Hare Krishna! Please submit your daily sadhana entry on the BhaktiVerse Devotee Dashboard.

   [DEVOTEE 1 SUBMITS Daily Sadhana Entry at 9:15 AM]

   [SIMULATING 10:00 AM - Japa Reminder #3]
EMAIL SENT ΓåÆ 8 AM sadhana reminder
EMAIL SENT ΓåÆ 8 AM sadhana reminder
EMAIL SENT ΓåÆ 8 AM sadhana reminder
EMAIL SENT ΓåÆ 8 AM sadhana reminder
      [EMAIL #1]
         Subject: Reminder: Submit Daily Sadhana
         To: ['devotee@example.com']
         Body Snippet: Hare Krishna! Please submit your daily sadhana entry on the BhaktiVerse Devotee Dashboard.
      [EMAIL #2]
         Subject: Reminder: Submit Daily Sadhana
         To: ['devotee_4005@example.com']
         Body Snippet: Hare Krishna! Please submit your daily sadhana entry on the BhaktiVerse Devotee Dashboard.
      [EMAIL #3]
         Subject: Reminder: Submit Daily Sadhana
         To: ['gsreyaskumar_cse235a0510@mgit.ac.in']
         Body Snippet: Hare Krishna! Please submit your daily sadhana entry on the BhaktiVerse Devotee Dashboard.
      [EMAIL #4]
         Subject: Reminder: Submit Daily Sadhana
         To: ['devotee_test2@bhaktiverse.com']
         Body Snippet: Hare Krishna! Please submit your daily sadhana entry on the BhaktiVerse Devotee Dashboard.

   [SIMULATING 11:00 AM - Japa Reminder #4]
EMAIL SENT ΓåÆ 8 AM sadhana reminder
EMAIL SENT ΓåÆ 8 AM sadhana reminder
EMAIL SENT ΓåÆ 8 AM sadhana reminder

--- ΓÜû∩╕Å Performance & Safety Verification ---
      [EMAIL #1]
         Subject: Reminder: Submit Daily Sadhana
         To: ['devotee@example.com']
         Body Snippet: Hare Krishna! Please submit your daily sadhana entry on the BhaktiVerse Devotee Dashboard.
      [EMAIL #2]
         Subject: Reminder: Submit Daily Sadhana
         To: ['devotee_4005@example.com']
         Body Snippet: Hare Krishna! Please submit your daily sadhana entry on the BhaktiVerse Devotee Dashboard.
      [EMAIL #3]
         Subject: Reminder: Submit Daily Sadhana
         To: ['gsreyaskumar_cse235a0510@mgit.ac.in']
         Body Snippet: Hare Krishna! Please submit your daily sadhana entry on the BhaktiVerse Devotee Dashboard.
      [EMAIL #4]
         Subject: Reminder: Submit Daily Sadhana
         To: ['devotee_test2@bhaktiverse.com']
         Body Snippet: Hare Krishna! Please submit your daily sadhana entry on the BhaktiVerse Devotee Dashboard.

   [SIMULATING 12:00 PM - Leader Summary Alert]
      [EMAIL #1]
         Subject: Devotees who did not submit Sadhana
         To: ['leader@example.com']
         Body Snippet: The following devotees have not submitted today's sadhana:
      [EMAIL #2]
         Subject: Devotees who did not submit Sadhana
         To: ['leader_4005@example.com']
         Body Snippet: The following devotees have not submitted today's sadhana:
      [EMAIL #3]
         Subject: Devotees who did not submit Sadhana
         To: ['gundasreyas@gmail.com']
         Body Snippet: The following devotees have not submitted today's sadhana:
      [EMAIL #4]
         Subject: Devotees who did not submit Sadhana
         To: ['temple_leader_test@bhaktiverse.com']
         Body Snippet: The following devotees have not submitted today's sadhana:
   Running duplicate summary scan at 12:01 PM...
   Duplicate summary emails: 0
   [PASS]: Japa JTR Reminders stop on submission, and Leader alert reports pending list accurately.
SCHEDULER RUNNING ΓåÆ scan_seva_duties
 Γ£ö BUG 1 (60-minute window limit): FIXED. Replaced range query with daily filter on service_date=today.
   Total Queries Executed: 7
   [PASS]: service_date index is strictly used. Full table scans are avoided.
   * Devotee Today Seva Count: 3

================================================================================
                      ALL TESTS EXECUTED SUCCESSFULLY
================================================================================

====================================================
                 FINAL VERIFICATION REPORT
====================================================

1. PASS/FAIL STATUS TABLE:
------------------------------------------------------------
 Scenario / Check                    | Status    
------------------------------------------------------------
 Scheduler Registration              | PASS      
 Timezone Awareness                  | PASS      
 Daily Assigned Service Mail         | PASS      
 10-Min Reminder Flow                | PASS      
 Overdue Failure Alert               | PASS      
 Sadhana Reminder System             | PASS      
 O(1) Service Date Scan              | PASS      
 Daily Reset & Dashboard Filters     | PASS      
------------------------------------------------------------

2. EXACT EMAILS TRIGGERED:
------------------------------------------------------------
 Email #1:
   Subject: 'New Service Assigned'
   To     : ['devotee_test1@bhaktiverse.com']
   Body   : You have been assigned the service: Morning Deity Altar Worship...
 Email #2:
   Subject: 'New Service Assigned'
   To     : ['devotee_test1@bhaktiverse.com']
   Body   : You have been assigned the service: Morning Deity Altar Worship...
 Email #3:
   Subject: 'Seva Reminder'
   To     : ['devotee_test1@bhaktiverse.com']
   Body   : Your service starts in 30 minutes....
 Email #4:
   Subject: 'Seva Started'
   To     : ['devotee_test1@bhaktiverse.com']
   Body   : Your service time has started....
 Email #5:
   Subject: 'Seva Reminder'
   To     : ['devotee_test1@bhaktiverse.com']
   Body   : Please remember to complete your ongoing service....
 Email #6:
   Subject: 'Service Not Completed'
   To     : ['temple_leader_test@bhaktiverse.com']
   Body   : Devotee did not complete assigned seva on time....
 Email #7:
   Subject: 'Reminder: Submit Daily Sadhana'
   To     : ['devotee@example.com']
   Body   : Hare Krishna! Please submit your daily sadhana entry on the BhaktiVerse Devotee Dashboard....
 Email #8:
   Subject: 'Reminder: Submit Daily Sadhana'
   To     : ['devotee_4005@example.com']
   Body   : Hare Krishna! Please submit your daily sadhana entry on the BhaktiVerse Devotee Dashboard....
 Email #9:
   Subject: 'Reminder: Submit Daily Sadhana'
   To     : ['gsreyaskumar_cse235a0510@mgit.ac.in']
   Body   : Hare Krishna! Please submit your daily sadhana entry on the BhaktiVerse Devotee Dashboard....
 Email #10:
   Subject: 'Reminder: Submit Daily Sadhana'
   To     : ['devotee_test1@bhaktiverse.com']
   Body   : Hare Krishna! Please submit your daily sadhana entry on the BhaktiVerse Devotee Dashboard....
 Email #11:
   Subject: 'Reminder: Submit Daily Sadhana'
   To     : ['devotee_test2@bhaktiverse.com']
   Body   : Hare Krishna! Please submit your daily sadhana entry on the BhaktiVerse Devotee Dashboard....
 Email #12:
   Subject: 'Reminder: Submit Daily Sadhana'
   To     : ['devotee@example.com']
   Body   : Hare Krishna! Please submit your daily sadhana entry on the BhaktiVerse Devotee Dashboard....
 Email #13:
   Subject: 'Reminder: Submit Daily Sadhana'
   To     : ['devotee_4005@example.com']
   Body   : Hare Krishna! Please submit your daily sadhana entry on the BhaktiVerse Devotee Dashboard....
 Email #14:
   Subject: 'Reminder: Submit Daily Sadhana'
   To     : ['gsreyaskumar_cse235a0510@mgit.ac.in']
   Body   : Hare Krishna! Please submit your daily sadhana entry on the BhaktiVerse Devotee Dashboard....
 Email #15:
   Subject: 'Reminder: Submit Daily Sadhana'
   To     : ['devotee_test1@bhaktiverse.com']
   Body   : Hare Krishna! Please submit your daily sadhana entry on the BhaktiVerse Devotee Dashboard....
 Email #16:
   Subject: 'Reminder: Submit Daily Sadhana'
   To     : ['devotee_test2@bhaktiverse.com']
   Body   : Hare Krishna! Please submit your daily sadhana entry on the BhaktiVerse Devotee Dashboard....
 Email #17:
   Subject: 'Reminder: Submit Daily Sadhana'
   To     : ['devotee@example.com']
   Body   : Hare Krishna! Please submit your daily sadhana entry on the BhaktiVerse Devotee Dashboard....
 Email #18:
   Subject: 'Reminder: Submit Daily Sadhana'
   To     : ['devotee_4005@example.com']
   Body   : Hare Krishna! Please submit your daily sadhana entry on the BhaktiVerse Devotee Dashboard....
 Email #19:
   Subject: 'Reminder: Submit Daily Sadhana'
   To     : ['gsreyaskumar_cse235a0510@mgit.ac.in']
   Body   : Hare Krishna! Please submit your daily sadhana entry on the BhaktiVerse Devotee Dashboard....
 Email #20:
   Subject: 'Reminder: Submit Daily Sadhana'
   To     : ['devotee_test2@bhaktiverse.com']
   Body   : Hare Krishna! Please submit your daily sadhana entry on the BhaktiVerse Devotee Dashboard....
 Email #21:
   Subject: 'Reminder: Submit Daily Sadhana'
   To     : ['devotee@example.com']
   Body   : Hare Krishna! Please submit your daily sadhana entry on the BhaktiVerse Devotee Dashboard....
 Email #22:
   Subject: 'Reminder: Submit Daily Sadhana'
   To     : ['devotee_4005@example.com']
   Body   : Hare Krishna! Please submit your daily sadhana entry on the BhaktiVerse Devotee Dashboard....
 Email #23:
   Subject: 'Reminder: Submit Daily Sadhana'
   To     : ['gsreyaskumar_cse235a0510@mgit.ac.in']
   Body   : Hare Krishna! Please submit your daily sadhana entry on the BhaktiVerse Devotee Dashboard....
 Email #24:
   Subject: 'Reminder: Submit Daily Sadhana'
   To     : ['devotee_test2@bhaktiverse.com']
   Body   : Hare Krishna! Please submit your daily sadhana entry on the BhaktiVerse Devotee Dashboard....
 Email #25:
   Subject: 'Devotees who did not submit Sadhana'
   To     : ['leader@example.com']
   Body   : The following devotees have not submitted today's sadhana:...
 Email #26:
   Subject: 'Devotees who did not submit Sadhana'
   To     : ['leader_4005@example.com']
   Body   : The following devotees have not submitted today's sadhana:...
 Email #27:
   Subject: 'Devotees who did not submit Sadhana'
   To     : ['gundasreyas@gmail.com']
   Body   : The following devotees have not submitted today's sadhana:...
 Email #28:
   Subject: 'Devotees who did not submit Sadhana'
   To     : ['temple_leader_test@bhaktiverse.com']
   Body   : The following devotees have not submitted today's sadhana:...
------------------------------------------------------------

3. DATABASE STATE TRANSITIONS:
------------------------------------------------------------
 ò WeeklySeva Day 1 assignment email status:
   - BEFORE: assignment_email_sent=False
   - AFTER : assignment_email_sent=True
 ò Seva Duty 10-Minute Reminder flow status transitions:
   - 09:30 AM: reminder_30_sent=True, status='pending'
   - 10:00 AM: reminder_start_sent=True, status='pending'
   - 10:10 AM: last_reminder_time=10:10 AM, status='pending'
   - 10:12 AM: status='completed', completed=True
   - 10:20 AM: no reminder sent (terminated due to complete)
   - 10:30 AM: no overdue alert sent (terminated due to complete)
 ò Overdue Seva Alert status transitions:
   - BEFORE: overdue_alert_sent=False, status='pending'
   - AFTER : overdue_alert_sent=True, status='pending' (Leader notified)
------------------------------------------------------------

4. BUGS FIXED AUTOMATICALLY:
------------------------------------------------------------
 Γ£ö BUG 2 (Japa hourly reminder gap): FIXED. Upgraded logic to scan hourly from 8:00 AM to 12:00 PM.
 Γ£ö BUG 3 (Japa reminder duplicates): FIXED. Added a 45-minute notification window lookup filter.
------------------------------------------------------------

5. FINAL CONFIRMATION:
 All scheduler, reminder, overdue, and sadhana systems verified successfully.
================================================================================
