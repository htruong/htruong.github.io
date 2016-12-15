// Huan's Poor man quote service

// What the Fuck Public license
//   0. You just DO WHAT THE FUCK YOU WANT TO.

function PoorManQuoteService() {
	this.quotes = [
		{
			"quote": "Anyone who has never made a mistake has never tried anything new.", 
			"author": "Albert Einstein"
		},
		{
			"quote": "The best time to plant a tree was 20 years ago. The second best time is now.", 
			"author": "Chinese Proverb"
		},
		{
			"quote": "You have to be twice as smart when debugging your code compared to when you wrote them.", 
			"author": "Gavin Conant, from colleague"
		},
		{
			"quote": "If the only tool you have is a hammer, you tend to see every problem as a nail.", "author": "Abraham H. Maslow"},
		{
			"quote": "The biggest mistake you can make is to always be right.", 
			"author": "Steve's Fortune Cookie, Bethesda Chinese Restaurant,1998"
		},
		{
			"quote": "Dogs do not dislike poor families.", 
			"author": "Chinese Proverb"
		},
		{
			"quote": "I've learned that people will forget what you said, people will forget what you did, but people will never forget how you made them feel.", 
			"author": "Maya Angelou"
		},
		{
			"quote": "Nothing in life is to be feared, it is only to be understood. Now is the time to understand more, so that we may fear less.", 
			"author": "Marie Curie"
		},
		{
			"quote": "Perl is like your messy bedroom that looks like a disaster to an outsider, but is perfectly logical and organized to you.", 
			"author": "Anon on /g/"
		},
		{
			"quote": "Find three hobbies you love: one to make you money, one to keep you in shape, and one to be creative.",
			"author": "American Nomad @coffee_n_mtns"
		},
		{
			"quote": "An engineer can do for a nickel what any damn fool can do for a dollar.", 
			"author": "Henry Ford"
		},
		{
			"quote": "If you can't explain it simply, you don't understand it well enough.", 
			"author": "Albert Einstein"
		},
		{
			"quote": "You can't have a better tomorrow if you are thinking about yesterday all the time.", 
			"author": "Charles F. Kettering"
		},
		{
			"quote": "A problem well stated is a problem half solved.", 
			"author": "Charles F. Kettering"
		},
		{
			"quote": "An inventor fails 999 times, and if he succeeds once, he's in. He treats his failures simply as practice shots.", 
			"author": "Charles F. Kettering"
		},
		{
			"quote": "Any application that can be written in JavaScript, will eventually be written in JavaScript.", 
			"author": "Jeff Atwood"
		},
		{
			"quote": "I have far more faith in xargs than I do in Hadoop. Hell, I trust xargs more than I trust myself to write a simple multithreaded processor. ", 
			"author": "Ted Dziuba"
		},
		{
			"quote": "I can remember when I had twenty followers that I didn’t know and I couldn’t believe there were twenty people who gave two shits about what I did.",
			"author": "Mule Dragger"
		}
	];
}

PoorManQuoteService.prototype.getRandomQuote = function() {
	return this.quotes[Math.floor( Math.random() * this.quotes.length )];
}

PoorManQuoteService.prototype.putRandomQuote = function(dest) {
	quote = this.getRandomQuote();
	dest.innerHTML = "<span class='poormanquote'><span class='quote'>" + quote.quote + "</span><span class='author'>" + quote.author + "</span></span>";
}

