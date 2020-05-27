/**
 *
 * 
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 * 
 *     http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package cdlinter.datamining.gitlab.entities;

public class Commit {

	private String message;

    private String id;

    private String author_email;

    private String title;

    private String committer_email;

    private String short_id;

    private String[] parent_ids;

    private String author_name;

    private String authored_date;

    private String created_at;

    private String committed_date;

    private String committer_name;

    public String getMessage ()
    {
        return message;
    }

    public void setMessage (String message)
    {
        this.message = message;
    }

    public String getId ()
    {
        return id;
    }

    public void setId (String id)
    {
        this.id = id;
    }

    public String getAuthor_email ()
    {
        return author_email;
    }

    public void setAuthor_email (String author_email)
    {
        this.author_email = author_email;
    }

    public String getTitle ()
    {
        return title;
    }

    public void setTitle (String title)
    {
        this.title = title;
    }

    public String getCommitter_email ()
    {
        return committer_email;
    }

    public void setCommitter_email (String committer_email)
    {
        this.committer_email = committer_email;
    }

    public String getShort_id ()
    {
        return short_id;
    }

    public void setShort_id (String short_id)
    {
        this.short_id = short_id;
    }

    public String[] getParent_ids ()
    {
        return parent_ids;
    }

    public void setParent_ids (String[] parent_ids)
    {
        this.parent_ids = parent_ids;
    }

    public String getAuthor_name ()
    {
        return author_name;
    }

    public void setAuthor_name (String author_name)
    {
        this.author_name = author_name;
    }

    public String getAuthored_date ()
    {
        return authored_date;
    }

    public void setAuthored_date (String authored_date)
    {
        this.authored_date = authored_date;
    }

    public String getCreated_at ()
    {
        return created_at;
    }

    public void setCreated_at (String created_at)
    {
        this.created_at = created_at;
    }

    public String getCommitted_date ()
    {
        return committed_date;
    }

    public void setCommitted_date (String committed_date)
    {
        this.committed_date = committed_date;
    }

    public String getCommitter_name ()
    {
        return committer_name;
    }

    public void setCommitter_name (String committer_name)
    {
        this.committer_name = committer_name;
    }

    @Override
    public String toString()
    {
        return "ClassPojo [message = "+message+", id = "+id+", author_email = "+author_email+", title = "+title+", committer_email = "+committer_email+", short_id = "+short_id+", parent_ids = "+parent_ids+", author_name = "+author_name+", authored_date = "+authored_date+", created_at = "+created_at+", committed_date = "+committed_date+", committer_name = "+committer_name+"]";
    }
    
}
