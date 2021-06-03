from paddlehub import Module


class Senta():
    """
    # Senta()
    @Description:
    a capsulation of paddlehub api, to provide a easier-to-use sentiment classifier.
    ---------
    @Params:
    No attributes need to set during constructing
    -------
    """

    def __init__(self) -> None:
        self.data = []
        self.classifier = Module(name="senta_bilstm")
        self.results = []

    def add(self, *sentences) -> None:
        """
        # Senta().add(sentences)
        @Description:
        add sentences to senta, preparing to be classified
        ---------
        @Param:
        `str`, or `list` consist of `str`s
        -------
        @Returns:
        `None`
        -------
        """
        for stc in sentences:
            if isinstance(stc, str):
                self.data.append(stc)
            elif isinstance(stc, list):
                for item in stc:
                    if isinstance(item, str):
                        self.data.append(item)

    def clear(self):
        """
        # Senta().clear()
        @Description:
        clear sentences data
        ---------
        @Param:
        `None`
        -------
        @Returns:
        `None`
        -------
        """
        self.data = []

    def predict(self) -> list:
        """
        # Senta().predict()
        @Description:
        predict the sentiment of the sentences stored in Senta
        and then DELETE THEM
        ---------
        @Param:
        No
        -------
        @Returns:
        `results`: a list consist of `dict`s with five key: 'text', 'sentiment_label', 'sentiment_key', 'positive_probs', 'negative_probs'
        -------
        """
        self.results = self.classifier.sentiment_classify(
            data={"text": self.data}) if self.data else []
        self.data = []
        return self.results

    def print(self):
        """
        # Senta().print()
        @Description:
        print results of the prediction
        ---------
        @Param:
        -------
        @Returns:
        -------
        """
        for result in self.results:
            print(result['text'])
            print(result['sentiment_label'])
            print(result['sentiment_key'])
            print(result['positive_probs'])
            print(result['negative_probs'])


if __name__ == "__main__":
    senta = Senta()
    senta.add(["余文乐患急性惊恐症", "稍微重了点，可能是硬盘大的原故，还要再轻半斤就好了。"])
    senta.predict()
    senta.print()