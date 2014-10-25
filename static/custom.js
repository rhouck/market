function gen_mail_to_link(lhs,rhs,subject)
	{
	document.write("<A HREF=\"mailto");
	document.write(":" + lhs + "@");
	document.write(rhs + "?subject=" + subject + "\">" + lhs + "@" + rhs + "<\/A>"); 
	} 
