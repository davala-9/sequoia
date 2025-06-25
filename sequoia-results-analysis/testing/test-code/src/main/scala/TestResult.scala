
class TestResult(success: String = "", hash: String = "", time: String = "", message: String = "", contextCount: Int = 0, selfMessages: Int = 0, otherMessages: Int = 0) {

  override def toString: String = { success + " , " + hash + " , " + time + " , " + message + " , " + contextCount + " , " + selfMessages + " , " + otherMessages}

  def hasSucceeded: Boolean = {success == "[SUCCESS]"}
}
