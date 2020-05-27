/**
 *
 * 
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not
 * use this file except in compliance with the License. You may obtain a copy of
 * the License at
 * 
 * http://www.apache.org/licenses/LICENSE-2.0
 * 
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations under
 * the License.
 */
package cdlinter.app;

import static cdlinter.app.VampirePusher.URL_VAMPIRE;
import static cdlinter.platform.parsers.AntiPattern2IssueConverter.convert;

import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;

import javax.ws.rs.client.Entity;
import javax.ws.rs.client.WebTarget;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;

import cdlinter.antipattern.entities.CIAntiPattern;
import cdlinter.antipattern.readers.CIAntiPatternCSVReader;
import cdlinter.platform.entities.Issue;
import me.tongfei.progressbar.ProgressBar;

public class run_VampirePush_for_internal {

	private WebTarget wt = VampirePusher.getWebTarget(URL_VAMPIRE);

	public static void main(String[] args) {
		new run_VampirePush_for_internal().run();
	}

	private void run() {
		Set<CIAntiPattern> cias = new CIAntiPatternCSVReader(run_sampling2.PATH_CIA_SAMPLED_INTERNAL).read();
		List<Issue> issues = cias.stream().map(cia -> convert(cia)).collect(Collectors.toList());

		ProgressBar pb = new ProgressBar("Pushing issues", issues.size());
		pb.start();

		for (Issue issue : issues) {
			pb.step();

			Entity<Issue> e = Entity.entity(issue, MediaType.APPLICATION_JSON);
			Response r = wt.request(MediaType.APPLICATION_JSON).accept(MediaType.APPLICATION_JSON).post(e);

			if (r.getStatus() != 200) {
				System.err.printf("`%s` could not be pushed (%d: %s)\n", issue.id, r.getStatus(),
						r.getStatusInfo().getReasonPhrase());
				continue;
			}
		}
		pb.stop();
	}

}